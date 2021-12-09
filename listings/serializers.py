from rest_framework import serializers

from listings.models import BookingInfo, Reserved, Listing

class BookingInfoSerializer(serializers.ModelSerializer):
    """
    BookingInfoSerializer
    """
    class Meta:

        model = BookingInfo
        fields = '__all__'

class ListingInfoSerializer(serializers.Serializer):
    """
    ListingInfoSerializer
    """
    listing_type = serializers.CharField(max_length=128, required=True)
    title = serializers.CharField(max_length=128, required=True)
    country = serializers.CharField(max_length=128, required=True)
    city = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:

        #model = Listing
        #fields = '__all__'
        fields = ('listing_type','title','country','city','price')


class ReservedSerializer(serializers.ModelSerializer):
    """
    ReservedSerializer
    """
    class Meta:

        model = Reserved
        fields = '__all__'
