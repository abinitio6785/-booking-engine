from datetime import datetime

from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from listings.models import BookingInfo, Reserved, Listing
from listings.serializers import BookingInfoSerializer, ReservedSerializer, ListingInfoSerializer


class BookingInfoViewSet(generics.ListAPIView):
    """
    BookingInfoViewSet
    """

    serializer_class = ListingInfoSerializer

    def get_queryset(self):
        max_price = self.request.query_params.get('max_price')
        check_in = self.request.query_params.get('check_in')
        check_out = self.request.query_params.get('check_out')

        if max_price and check_in and check_out:
            query = "SELECT \
                listing.id, listing.title, listing.listing_type, \
                CASE listing_type \
                WHEN 'apartment' THEN (SELECT price FROM listings_bookinginfo where listing_id = listing.id) \
                WHEN 'hotel' THEN (SELECT MIN(price) FROM listings_bookinginfo where hotel_room_type_id IN \
                    (SELECT listings_hotelroomtype.id FROM listings_hotelroomtype where hotel_id = listing.id \
                        AND listings_hotelroomtype.id NOT IN (SELECT hotel_room_id_id FROM listings_reserved as res \
                        where(res.check_out BETWEEN '%s' and '%s') and \
                        (res.check_in BETWEEN '%s' and '%s'))) \
                ) \
                ELSE NULL \
                END as 'price' \
                FROM listings_listing as listing \
                GROUP BY listing.id \
                HAVING MIN (price)< %s" %(check_in, check_out, check_in, check_out, max_price)
        else:
            query = "SELECT \
                listing.id, listing.title, listing.listing_type, \
                CASE listing_type \
                WHEN 'apartment' THEN (SELECT price FROM listings_bookinginfo where listing_id = listing.id) \
                WHEN 'hotel' THEN (SELECT MIN(price) FROM listings_bookinginfo where hotel_room_type_id IN \
                    (SELECT listings_hotelroomtype.id FROM listings_hotelroomtype where hotel_id = listing.id \
                )) \
                ELSE NULL \
                END as 'price' \
                FROM listings_listing as listing \
                GROUP BY listing.id \
                HAVING MIN (price)< %s" %max_price

        queryset = Listing.objects.raw(query)

        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        # the serializer didn't take my RawQuerySet, so made it into a list
        serializer = ListingInfoSerializer(list(queryset), many=True)
        return Response(serializer.data)


class ReservedInfoViewSet(generics.ListCreateAPIView):
    """
    ReservedInfoViewSet
    """
    serializer_class = ReservedSerializer
    queryset = Reserved.objects.all()
