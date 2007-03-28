#!/usr/bin/env python
# -*- coding: utf-8 -*

############################################################################
# Joshua R. Boverhof, LBNL
# See LBNLCopyright for copyright notice!
###########################################################################
import sys, unittest
from ServiceTest import main, ServiceTestCase, ServiceTestSuite, TestException
from ZSI.schema import ElementDeclaration, GED
from ZSI import ParsedSoap

"""
Unittest for contacting the Amazon ECommerce Service

WSDL: 

"""
# General targets
def dispatch():
    """Run all dispatch tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(AmazonTestCase, 'test_dispatch'))
    return suite

def local():
    """Run all local tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(AmazonTestCase, 'test_local'))
    return suite

def net():
    """Run all network tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(AmazonTestCase, 'test_net'))
    return suite
    
def all():
    """Run all tests"""
    suite = ServiceTestSuite()
    suite.addTest(unittest.makeSuite(AmazonTestCase, 'test_'))
    return suite


TargetNamespace = "http://webservices.amazon.com/AWSECommerceService/2007-02-22"
class AmazonTestCase(ServiceTestCase):
    """Test case for Amazon ECommerce Web service
    """
    name = "test_AWSECommerceService"
    client_file_name = "AWSECommerceService_client.py"
    types_file_name  = "AWSECommerceService_types.py"
    server_file_name = "AWSECommerceService_server.py"

    def __init__(self, methodName):
        ServiceTestCase.__init__(self, methodName)
        self.wsdl2py_args.append('-b')
        self.wsdl2py_args.append('--lazy')

    def test_local_bug_1525567(self):
        element = GED(TargetNamespace, 'Items')
        # Make sure this is a GED
        self.failUnless(isinstance(element, ElementDeclaration), '"%s" not a GED' %element)
    
    def test_local_parse_ItemSearch(self):
        msg = self.client_module.ItemSearchResponseMsg()
        ps = ParsedSoap(ItemSearchResponseMsg)
        response = ps.Parse(msg.typecode)
        response.OperationRequest.Arguments
        for i in response.OperationRequest.Arguments.Argument: 
             i.get_attribute_Name()
             i.get_attribute_Value()

        for i in response.OperationRequest.HTTPHeaders.Header or []:
             i.get_attribute_Name()
             i.get_attribute_Value()
             
        response.OperationRequest.RequestId
        response.OperationRequest.RequestProcessingTime
        for its in response.Items:
            self.failUnless(its.TotalResults == 61, '')
            self.failUnless(its.TotalPages == 7, '')
            for it in its.Item:
                it.ASIN; 
                it.Accessories; 
                #it.AlternateVersions; 
                it.BrowseNodes
                #it.Collections; 
                it.CustomerReviews ;it.DetailPageURL
                it.EditorialReviews; it.Errors; it.ImageSets; it.ItemAttributes
                it.LargeImage; it.ListmaniaLists; it.MediumImage; it.MerchantItemAttributes
                it.OfferSummary; it.Offers; 
                #it.ParentASIN; 
                it.SalesRank; it.SearchInside
                it.SimilarProducts; it.SmallImage; it.Subjects; it.Tracks;


    def test_net_ItemSearch(self):
        loc = self.client_module.AWSECommerceServiceLocator()
        port = loc.getAWSECommerceServicePort(**self.getPortKWArgs())

        msg = self.client_module.ItemSearchRequestMsg()
        msg.SubscriptionId = '0HP1WHME000749APYWR2'
        request = msg.new_Request()
        msg.Request = [request]

        # request
        request.ItemPage = 1
        request.SearchIndex = "Books"
        request.Keywords = 'Tamerlane'
        request.ResponseGroup = ['Medium',]

        response = port.ItemSearch(msg)

        response.OperationRequest
        self.failUnless(response.OperationRequest.Errors is None, 'ecommerce site reported errors')

        response.OperationRequest.Arguments
        for i in response.OperationRequest.Arguments.Argument: 
             i.get_attribute_Name()
             i.get_attribute_Value()

        for i in response.OperationRequest.HTTPHeaders.Header or []:
             i.get_attribute_Name()
             i.get_attribute_Value()
             
        response.OperationRequest.RequestId
        response.OperationRequest.RequestProcessingTime
        for its in response.Items:
            for it in its.Item:
                it.ASIN; 
                it.Accessories; 
                #it.AlternateVersions; 
                it.BrowseNodes
                #it.Collections; 
                it.CustomerReviews ;it.DetailPageURL
                it.EditorialReviews; it.Errors; it.ImageSets; it.ItemAttributes
                it.LargeImage; it.ListmaniaLists; it.MediumImage; it.MerchantItemAttributes
                it.OfferSummary; it.Offers; 
                #it.ParentASIN; 
                it.SalesRank; it.SearchInside
                it.SimilarProducts; it.SmallImage; it.Subjects; it.Tracks;
                it.VariationSummary; it.Variations


ItemSearchResponseMsg="""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xmlns:xsd="http://www.w3.org/2001/XMLSchema"><SOAP-ENV:Body><ItemSearchResponse xmlns="http://webservices.amazon.com/AWSECommerceService/2007-02-22"><OperationRequest><HTTPHeaders><Header Name="UserAgent"></Header></HTTPHeaders><RequestId>013FGTRCYPQV2EFA975Q</RequestId><Arguments><Argument Name="Service" Value="AWSECommerceService"></Argument></Arguments><RequestProcessingTime>0.353393793106079</RequestProcessingTime></OperationRequest><Items><Request><IsValid>True</IsValid><ItemSearchRequest><ItemPage>1</ItemPage><Keywords>Tamerlane</Keywords><ResponseGroup>Medium</ResponseGroup><SearchIndex>Books</SearchIndex></ItemSearchRequest></Request><TotalResults>61</TotalResults><TotalPages>7</TotalPages><Item><ASIN>030681465X</ASIN><DetailPageURL>http://www.amazon.com/gp/redirect.html%3FASIN=030681465X%26tag=ws%26lcode=sp1%26cID=2025%26ccmID=165953%26location=/o/ASIN/030681465X%253FSubscriptionId=0HP1WHME000749APYWR2</DetailPageURL><SalesRank>262921</SalesRank><SmallImage><URL>http://ec1.images-amazon.com/images/P/030681465X.01._SCTHUMBZZZ_V66860320_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">50</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/030681465X.01._SCMZZZZZZZ_V66860320_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">108</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/030681465X.01._SCLZZZZZZZ_V66860320_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">337</Width></LargeImage><ImageSets><ImageSet Category="primary"><SwatchImage><URL>http://ec1.images-amazon.com/images/P/030681465X.01._SCSWATCHZZ_V66860320_.jpg</URL><Height Units="pixels">30</Height><Width Units="pixels">20</Width></SwatchImage><SmallImage><URL>http://ec1.images-amazon.com/images/P/030681465X.01._SCTHUMBZZZ_V66860320_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">50</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/030681465X.01._SCMZZZZZZZ_V66860320_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">108</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/030681465X.01._SCLZZZZZZZ_V66860320_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">337</Width></LargeImage></ImageSet></ImageSets><ItemAttributes><Author>Justin Marozzi</Author><Binding>Hardcover</Binding><DeweyDecimalNumber>920</DeweyDecimalNumber><EAN>9780306814655</EAN><Edition>New Ed</Edition><ISBN>030681465X</ISBN><Label>Da Capo Press</Label><ListPrice><Amount>2695</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$26.95</FormattedPrice></ListPrice><Manufacturer>Da Capo Press</Manufacturer><NumberOfItems>1</NumberOfItems><NumberOfPages>368</NumberOfPages><PackageDimensions><Height Units="hundredths-inches">150</Height><Length Units="hundredths-inches">904</Length><Weight Units="hundredths-pounds">174</Weight><Width Units="hundredths-inches">640</Width></PackageDimensions><ProductGroup>Book</ProductGroup><PublicationDate>2006-02-22</PublicationDate><Publisher>Da Capo Press</Publisher><Studio>Da Capo Press</Studio><Title>Tamerlane: Sword of Islam, Conqueror of the World</Title></ItemAttributes><OfferSummary><LowestNewPrice><Amount>399</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$3.99</FormattedPrice></LowestNewPrice><LowestUsedPrice><Amount>399</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$3.99</FormattedPrice></LowestUsedPrice><LowestCollectiblePrice><Amount>2695</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$26.95</FormattedPrice></LowestCollectiblePrice><TotalNew>31</TotalNew><TotalUsed>24</TotalUsed><TotalCollectible>1</TotalCollectible><TotalRefurbished>0</TotalRefurbished></OfferSummary><EditorialReviews><EditorialReview><Source>Book Description</Source><Content>A powerful account of the life of Tamerlane the Great (1336-1405), the last great Mongol conqueror of Central Asia, ruler of a vast empire, and one of history's most brutal tyrants &lt;P&gt; Tamerlane, aka Temur-the Mongol successor to Genghis Khan-ranks with Alexander the Great as one of the world's great conquerors, yet the details of his life are scarcely known in the West. Born in obscurity and poverty, he rose to become a fierce tribal leader, and with that his dominion and power grew with astonishing speed. He blazed through Asia, razing cities to the ground. He tortured conquered inhabitants without mercy, sometimes ordering them buried alive, at other times decapitating them. Over the ruins of conquered Baghdad, Tamerlane had his soldiers erect a pyramid of 90,000 enemy heads. As he and his armies swept through Central Asia, sacking, and then rebuilding cities, Tamerlane gradually imposed an iron rule and a refined culture over a vast territory-from the steppes of Asia to the Syrian coastline. &lt;P&gt; Justin Marozzi traveled in the footsteps of this fearsome emperor of Samarkand (modern-day Uzbekistan) to write this book, which is part history, part travelogue. He carefully follows the path of this infamous and enigmatic conqueror, recounting the history and the story of this cruel, cultivated, and indomitable warrior.</Content></EditorialReview></EditorialReviews></Item><Item><ASIN>1851684573</ASIN><DetailPageURL>http://www.amazon.com/gp/redirect.html%3FASIN=1851684573%26tag=ws%26lcode=sp1%26cID=2025%26ccmID=165953%26location=/o/ASIN/1851684573%253FSubscriptionId=0HP1WHME000749APYWR2</DetailPageURL><SalesRank>567693</SalesRank><SmallImage><URL>http://ec1.images-amazon.com/images/P/1851684573.01._SCTHUMBZZZ_V63318467_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">49</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/1851684573.01._SCMZZZZZZZ_V63318467_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">104</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/1851684573.01._SCLZZZZZZZ_V63318467_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">324</Width></LargeImage><ImageSets><ImageSet Category="primary"><SwatchImage><URL>http://ec1.images-amazon.com/images/P/1851684573.01._SCSWATCHZZ_V63318467_.jpg</URL><Height Units="pixels">30</Height><Width Units="pixels">20</Width></SwatchImage><SmallImage><URL>http://ec1.images-amazon.com/images/P/1851684573.01._SCTHUMBZZZ_V63318467_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">49</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/1851684573.01._SCMZZZZZZZ_V63318467_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">104</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/1851684573.01._SCLZZZZZZZ_V63318467_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">324</Width></LargeImage></ImageSet></ImageSets><ItemAttributes><Author>Robert Rand</Author><Binding>Paperback</Binding><DeweyDecimalNumber>958.7086</DeweyDecimalNumber><EAN>9781851684571</EAN><ISBN>1851684573</ISBN><Label>Oneworld Publications</Label><ListPrice><Amount>1495</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$14.95</FormattedPrice></ListPrice><Manufacturer>Oneworld Publications</Manufacturer><NumberOfItems>1</NumberOfItems><NumberOfPages>224</NumberOfPages><PackageDimensions><Height Units="hundredths-inches">66</Height><Length Units="hundredths-inches">784</Length><Weight Units="hundredths-pounds">54</Weight><Width Units="hundredths-inches">512</Width></PackageDimensions><ProductGroup>Book</ProductGroup><PublicationDate>2006-09-11</PublicationDate><Publisher>Oneworld Publications</Publisher><Studio>Oneworld Publications</Studio><Title>Tamerlane's Children: Dispatches from Contemporary Uzbekistan</Title></ItemAttributes><OfferSummary><LowestNewPrice><Amount>708</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$7.08</FormattedPrice></LowestNewPrice><LowestUsedPrice><Amount>708</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$7.08</FormattedPrice></LowestUsedPrice><LowestCollectiblePrice><Amount>1495</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$14.95</FormattedPrice></LowestCollectiblePrice><TotalNew>31</TotalNew><TotalUsed>9</TotalUsed><TotalCollectible>1</TotalCollectible><TotalRefurbished>0</TotalRefurbished></OfferSummary><EditorialReviews><EditorialReview><Source>Book Description</Source><Content>In the central park of Tashkent, in a place the Uzbeks call the square, a magnificent statue of a mounted warrior dominates the surroundings - Tamerlane - national hero of post-Soviet Uzbekistan. And yet how does this 14th century conqueror reflect one of the world's most diverse and politically intriguing countries?Having spent three years in the region, renowned journalist Robert Rand seeks to answer this question, covering an assortment of fascinating topics, ranging from the effect of 9/11 to the clash of culture in Uzbek pop music.  Overflowing with charming anecdotes and loveable personalities, Rand gives the reader a real sense of the country's confused identity and  the challenges which it and its people will face in generations to come.</Content></EditorialReview></EditorialReviews></Item><Item><ASIN>0521633842</ASIN><DetailPageURL>http://www.amazon.com/gp/redirect.html%3FASIN=0521633842%26tag=ws%26lcode=sp1%26cID=2025%26ccmID=165953%26location=/o/ASIN/0521633842%253FSubscriptionId=0HP1WHME000749APYWR2</DetailPageURL><SalesRank>584780</SalesRank><SmallImage><URL>http://ec1.images-amazon.com/images/P/0521633842.01._SCTHUMBZZZ_V1114821525_.jpg</URL><Height Units="pixels">60</Height><Width Units="pixels">39</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/0521633842.01._SCMZZZZZZZ_V1114821525_.jpg</URL><Height Units="pixels">140</Height><Width Units="pixels">90</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/0521633842.01._SCLZZZZZZZ_V1114821525_.jpg</URL><Height Units="pixels">475</Height><Width Units="pixels">306</Width></LargeImage><ImageSets><ImageSet Category="primary"><SwatchImage><URL>http://ec1.images-amazon.com/images/P/0521633842.01._SCSWATCHZZ_V1114821525_.jpg</URL><Height Units="pixels">30</Height><Width Units="pixels">19</Width></SwatchImage><SmallImage><URL>http://ec1.images-amazon.com/images/P/0521633842.01._SCTHUMBZZZ_V1114821525_.jpg</URL><Height Units="pixels">60</Height><Width Units="pixels">39</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/0521633842.01._SCMZZZZZZZ_V1114821525_.jpg</URL><Height Units="pixels">140</Height><Width Units="pixels">90</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/0521633842.01._SCLZZZZZZZ_V1114821525_.jpg</URL><Height Units="pixels">475</Height><Width Units="pixels">306</Width></LargeImage></ImageSet></ImageSets><ItemAttributes><Author>Beatrice Forbes Manz</Author><Binding>Paperback</Binding><DeweyDecimalNumber>950.2</DeweyDecimalNumber><EAN>9780521633840</EAN><Edition>Reprint</Edition><ISBN>0521633842</ISBN><Label>Cambridge University Press</Label><ListPrice><Amount>2499</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$24.99</FormattedPrice></ListPrice><Manufacturer>Cambridge University Press</Manufacturer><NumberOfItems>1</NumberOfItems><NumberOfPages>248</NumberOfPages><PackageDimensions><Height Units="hundredths-inches">67</Height><Length Units="hundredths-inches">850</Length><Weight Units="hundredths-pounds">74</Weight><Width Units="hundredths-inches">562</Width></PackageDimensions><ProductGroup>Book</ProductGroup><PublicationDate>2002-10-26</PublicationDate><Publisher>Cambridge University Press</Publisher><ReleaseDate>2002-10-26</ReleaseDate><Studio>Cambridge University Press</Studio><Title>Rise and Rule of Tamerlane, The (Canto original series)</Title></ItemAttributes><OfferSummary><LowestNewPrice><Amount>1950</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$19.50</FormattedPrice></LowestNewPrice><LowestUsedPrice><Amount>869</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$8.69</FormattedPrice></LowestUsedPrice><LowestCollectiblePrice><Amount>2499</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$24.99</FormattedPrice></LowestCollectiblePrice><TotalNew>22</TotalNew><TotalUsed>23</TotalUsed><TotalCollectible>2</TotalCollectible><TotalRefurbished>0</TotalRefurbished></OfferSummary><EditorialReviews><EditorialReview><Source>Book Description</Source><Content>This is the first serious study of Tamerlane, the great nomad conqueror who rose to power in 1370 on the ruins of the Mongol Empire and led his armies on campaigns of unprecedented scope, ranging from Moscow to Delhi.  As the last nomad ruler to unite the steppe regions of Eurasia, Tamerlane marks the transition from the era of nomad conquest and rule to the modern ascendency of the settled world.</Content></EditorialReview></EditorialReviews></Item><Item><ASIN>189226420X</ASIN><DetailPageURL>http://www.amazon.com/gp/redirect.html%3FASIN=189226420X%26tag=ws%26lcode=sp1%26cID=2025%26ccmID=165953%26location=/o/ASIN/189226420X%253FSubscriptionId=0HP1WHME000749APYWR2</DetailPageURL><SalesRank>817168</SalesRank><SmallImage><URL>http://ec1.images-amazon.com/images/P/189226420X.01._SCTHUMBZZZ_V40073149_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">50</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/189226420X.01._SCMZZZZZZZ_V40073149_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">107</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/189226420X.01._SCLZZZZZZZ_V40073149_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">333</Width></LargeImage><ImageSets><ImageSet Category="primary"><SwatchImage><URL>http://ec1.images-amazon.com/images/P/189226420X.01._SCSWATCHZZ_V40073149_.jpg</URL><Height Units="pixels">30</Height><Width Units="pixels">20</Width></SwatchImage><SmallImage><URL>http://ec1.images-amazon.com/images/P/189226420X.01._SCTHUMBZZZ_V40073149_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">50</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/189226420X.01._SCMZZZZZZZ_V40073149_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">107</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/189226420X.01._SCLZZZZZZZ_V40073149_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">333</Width></LargeImage></ImageSet></ImageSets><ItemAttributes><Author>Roy Stier</Author><Binding>Paperback</Binding><DeweyDecimalNumber>930</DeweyDecimalNumber><EAN>9781892264206</EAN><ISBN>189226420X</ISBN><Label>Timeless Voyager Press</Label><ListPrice><Amount>1200</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$12.00</FormattedPrice></ListPrice><Manufacturer>Timeless Voyager Press</Manufacturer><NumberOfItems>1</NumberOfItems><NumberOfPages>356</NumberOfPages><PackageDimensions><Height Units="hundredths-inches">79</Height><Length Units="hundredths-inches">900</Length><Weight Units="hundredths-pounds">115</Weight><Width Units="hundredths-inches">600</Width></PackageDimensions><ProductGroup>Book</ProductGroup><PublicationDate>2006-09-05</PublicationDate><Publisher>Timeless Voyager Press</Publisher><ReleaseDate>2006-09-21</ReleaseDate><Studio>Timeless Voyager Press</Studio><Title>Tamerlane: The Ultimate Warrior- Map Edition</Title></ItemAttributes><OfferSummary><LowestNewPrice><Amount>832</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$8.32</FormattedPrice></LowestNewPrice><LowestUsedPrice><Amount>862</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$8.62</FormattedPrice></LowestUsedPrice><LowestCollectiblePrice><Amount>1200</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$12.00</FormattedPrice></LowestCollectiblePrice><TotalNew>17</TotalNew><TotalUsed>8</TotalUsed><TotalCollectible>1</TotalCollectible><TotalRefurbished>0</TotalRefurbished></OfferSummary><EditorialReviews><EditorialReview><Source>Book Description</Source><Content>Tamerlane: The Ultimate Warrior- Map Edition (978-1-892264-20-6) In this Third Edition, little-known fourteenth century Muslim leader who inspired a vast army of Islamic followers to swarm through central and western Asia in a conquering wave, has been captured in the first complete history using narrative form by Roy Stier. Tamerlane, the Ultimate Warrior paints the violent and controversial true story of the swift horseman who threatened much of the Old World, crushing the Ottoman Empire and intimidating kings and emperors. A trail of devastation followed the ruthless conqueror from Delhi to Baghdad, yet incidents of mercy for his enemies revealed a benign side to Tamerlane. In the pageantry of rulers, Tamerlane found little recognition from the historians of later centuries. Killer? Demonic? ¿ or charismatic visionary with a flashing sword and a view of the world united under the banner of Islamic purity? Is there a message for moderns in the story of the military genius who scythed his way through a sizable part of the known world? The readers of this book think so. There are 9 illustrations and photographs, 28 new maps of the ancient world circa 1300 A.D., complete references for researchers, glossary of terms, four appendices, a complete chronology of events, and an index in the 354 page 6¿ X 9¿ book. Retail price: $21.95 plus S/H.</Content></EditorialReview></EditorialReviews></Item><Item><ASIN>B00087SKA2</ASIN><DetailPageURL>http://www.amazon.com/gp/redirect.html%3FASIN=B00087SKA2%26tag=ws%26lcode=sp1%26cID=2025%26ccmID=165953%26location=/o/ASIN/B00087SKA2%253FSubscriptionId=0HP1WHME000749APYWR2</DetailPageURL><SalesRank>955067</SalesRank><ItemAttributes><Author>Harold Lamb</Author><Binding>Unknown Binding</Binding><Label>Bantam Books</Label><Manufacturer>Bantam Books</Manufacturer><NumberOfPages>216</NumberOfPages><ProductGroup>Book</ProductGroup><PublicationDate>1955</PublicationDate><Publisher>Bantam Books</Publisher><Studio>Bantam Books</Studio><Title>Tamerlane: Conqueror of the earth</Title></ItemAttributes><OfferSummary><LowestUsedPrice><Amount>795</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$7.95</FormattedPrice></LowestUsedPrice><TotalNew>0</TotalNew><TotalUsed>3</TotalUsed><TotalCollectible>0</TotalCollectible><TotalRefurbished>0</TotalRefurbished></OfferSummary></Item><Item><ASIN>0850459494</ASIN><DetailPageURL>http://www.amazon.com/gp/redirect.html%3FASIN=0850459494%26tag=ws%26lcode=sp1%26cID=2025%26ccmID=165953%26location=/o/ASIN/0850459494%253FSubscriptionId=0HP1WHME000749APYWR2</DetailPageURL><SalesRank>230563</SalesRank><SmallImage><URL>http://ec1.images-amazon.com/images/P/0850459494.01._SCTHUMBZZZ_V1128022797_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">56</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/0850459494.01._SCMZZZZZZZ_V1128022797_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">119</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/0850459494.01._SCLZZZZZZZ_V1128022797_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">372</Width></LargeImage><ImageSets><ImageSet Category="primary"><SwatchImage><URL>http://ec1.images-amazon.com/images/P/0850459494.01._SCSWATCHZZ_V1128022797_.jpg</URL><Height Units="pixels">30</Height><Width Units="pixels">22</Width></SwatchImage><SmallImage><URL>http://ec1.images-amazon.com/images/P/0850459494.01._SCTHUMBZZZ_V1128022797_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">56</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/0850459494.01._SCMZZZZZZZ_V1128022797_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">119</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/0850459494.01._SCLZZZZZZZ_V1128022797_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">372</Width></LargeImage></ImageSet></ImageSets><ItemAttributes><Author>David Nicolle</Author><Binding>Paperback</Binding><Creator Role="Illustrator">Angus Mcbride</Creator><EAN>9780850459494</EAN><ISBN>0850459494</ISBN><Label>Osprey Publishing</Label><ListPrice><Amount>1595</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$15.95</FormattedPrice></ListPrice><Manufacturer>Osprey Publishing</Manufacturer><NumberOfItems>1</NumberOfItems><NumberOfPages>48</NumberOfPages><PackageDimensions><Height Units="hundredths-inches">15</Height><Length Units="hundredths-inches">978</Length><Weight Units="hundredths-pounds">36</Weight><Width Units="hundredths-inches">722</Width></PackageDimensions><ProductGroup>Book</ProductGroup><PublicationDate>1990-07-26</PublicationDate><Publisher>Osprey Publishing</Publisher><ReleaseDate>1990-07-26</ReleaseDate><Studio>Osprey Publishing</Studio><Title>The Age of Tamerlane (Men-at-Arms)</Title></ItemAttributes><OfferSummary><LowestNewPrice><Amount>900</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$9.00</FormattedPrice></LowestNewPrice><LowestUsedPrice><Amount>1200</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$12.00</FormattedPrice></LowestUsedPrice><TotalNew>4</TotalNew><TotalUsed>3</TotalUsed><TotalCollectible>0</TotalCollectible><TotalRefurbished>0</TotalRefurbished></OfferSummary><EditorialReviews><EditorialReview><Source>Book Description</Source><Content>Tamerlane or Timur-i-Lenk ('Timur the Lame') is one of the most extraordinary conquerors in history. In the late 14th century his armies seized huge territories from the borders of Mongolia to Palestine and Anatolia. His passage was marked by massacres that outdid even those of the Mongols for sheer savagery. Timur's career was unequalled since Alexander the Great in terms of constant battlefield success. Only in his youth, while recovering his family estates south of Samarqand, did he face occasional defeat. This title tells the remarkable story of Timur and details the organisation, tactics, arms and armour of his all-conquering army.</Content></EditorialReview></EditorialReviews></Item><Item><ASIN>1410222950</ASIN><DetailPageURL>http://www.amazon.com/gp/redirect.html%3FASIN=1410222950%26tag=ws%26lcode=sp1%26cID=2025%26ccmID=165953%26location=/o/ASIN/1410222950%253FSubscriptionId=0HP1WHME000749APYWR2</DetailPageURL><SalesRank>665664</SalesRank><SmallImage><URL>http://ec1.images-amazon.com/images/P/1410222950.01._SCTHUMBZZZ_V1120611566_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">50</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/1410222950.01._SCMZZZZZZZ_V1120611566_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">107</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/1410222950.01._SCLZZZZZZZ_V1120611566_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">333</Width></LargeImage><ImageSets><ImageSet Category="primary"><SwatchImage><URL>http://ec1.images-amazon.com/images/P/1410222950.01._SCSWATCHZZ_V1120611566_.jpg</URL><Height Units="pixels">30</Height><Width Units="pixels">20</Width></SwatchImage><SmallImage><URL>http://ec1.images-amazon.com/images/P/1410222950.01._SCTHUMBZZZ_V1120611566_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">50</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/1410222950.01._SCMZZZZZZZ_V1120611566_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">107</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/1410222950.01._SCLZZZZZZZ_V1120611566_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">333</Width></LargeImage></ImageSet></ImageSets><ItemAttributes><Binding>Paperback</Binding><Creator Role="Editor">Daniel L. Burghart</Creator><Creator Role="Editor">Theresa Sabonis-helf</Creator><DeweyDecimalNumber>327</DeweyDecimalNumber><EAN>9781410222954</EAN><ISBN>1410222950</ISBN><Label>University Press of the Pacific</Label><ListPrice><Amount>3450</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$34.50</FormattedPrice></ListPrice><Manufacturer>University Press of the Pacific</Manufacturer><NumberOfItems>1</NumberOfItems><NumberOfPages>504</NumberOfPages><PackageDimensions><Height Units="hundredths-inches">112</Height><Length Units="hundredths-inches">900</Length><Weight Units="hundredths-pounds">161</Weight><Width Units="hundredths-inches">600</Width></PackageDimensions><ProductGroup>Book</ProductGroup><PublicationDate>2005-05-31</PublicationDate><Publisher>University Press of the Pacific</Publisher><Studio>University Press of the Pacific</Studio><Title>In the Tracks of Tamerlane: Central Asia's Path to the 21st Century</Title></ItemAttributes><OfferSummary><LowestNewPrice><Amount>2995</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$29.95</FormattedPrice></LowestNewPrice><LowestUsedPrice><Amount>4062</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$40.62</FormattedPrice></LowestUsedPrice><TotalNew>15</TotalNew><TotalUsed>7</TotalUsed><TotalCollectible>0</TotalCollectible><TotalRefurbished>0</TotalRefurbished></OfferSummary></Item><Item><ASIN>1853141046</ASIN><DetailPageURL>http://www.amazon.com/gp/redirect.html%3FASIN=1853141046%26tag=ws%26lcode=sp1%26cID=2025%26ccmID=165953%26location=/o/ASIN/1853141046%253FSubscriptionId=0HP1WHME000749APYWR2</DetailPageURL><SalesRank>980362</SalesRank><ItemAttributes><Author>David Nicolle</Author><Author>Richard Hook</Author><Binding>Hardcover</Binding><DeweyDecimalNumber>950.20922</DeweyDecimalNumber><EAN>9781853141041</EAN><ISBN>1853141046</ISBN><Label>Firebird</Label><ListPrice><Amount>2495</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$24.95</FormattedPrice></ListPrice><Manufacturer>Firebird</Manufacturer><NumberOfItems>1</NumberOfItems><NumberOfPages>208</NumberOfPages><PackageDimensions><Height Units="hundredths-inches">1000</Height><Length Units="hundredths-inches">75</Length><Weight Units="hundredths-pounds">160</Weight><Width Units="hundredths-inches">775</Width></PackageDimensions><ProductGroup>Book</ProductGroup><PublicationDate>1990-09</PublicationDate><Publisher>Firebird</Publisher><Studio>Firebird</Studio><Title>The Mongol Warlords: Ghengis Khan, Kublai Khan, Hulegu, Tamerlane (Heroes &amp; Warriors)</Title></ItemAttributes><OfferSummary><LowestUsedPrice><Amount>4700</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$47.00</FormattedPrice></LowestUsedPrice><TotalNew>0</TotalNew><TotalUsed>4</TotalUsed><TotalCollectible>0</TotalCollectible><TotalRefurbished>0</TotalRefurbished></OfferSummary></Item><Item><ASIN>0306815435</ASIN><DetailPageURL>http://www.amazon.com/gp/redirect.html%3FASIN=0306815435%26tag=ws%26lcode=sp1%26cID=2025%26ccmID=165953%26location=/o/ASIN/0306815435%253FSubscriptionId=0HP1WHME000749APYWR2</DetailPageURL><SalesRank>503889</SalesRank><SmallImage><URL>http://ec1.images-amazon.com/images/P/0306815435.01._SCTHUMBZZZ_V35579588_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">50</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/0306815435.01._SCMZZZZZZZ_V35579588_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">107</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/0306815435.01._SCLZZZZZZZ_V35579588_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">333</Width></LargeImage><ImageSets><ImageSet Category="primary"><SwatchImage><URL>http://ec1.images-amazon.com/images/P/0306815435.01._SCSWATCHZZ_V35579588_.jpg</URL><Height Units="pixels">30</Height><Width Units="pixels">20</Width></SwatchImage><SmallImage><URL>http://ec1.images-amazon.com/images/P/0306815435.01._SCTHUMBZZZ_V35579588_.jpg</URL><Height Units="pixels">75</Height><Width Units="pixels">50</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/0306815435.01._SCMZZZZZZZ_V35579588_.jpg</URL><Height Units="pixels">160</Height><Width Units="pixels">107</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/0306815435.01._SCLZZZZZZZ_V35579588_.jpg</URL><Height Units="pixels">500</Height><Width Units="pixels">333</Width></LargeImage></ImageSet></ImageSets><ItemAttributes><Author>Justin Marozzi</Author><Binding>Paperback</Binding><DeweyDecimalNumber>920</DeweyDecimalNumber><EAN>9780306815430</EAN><Edition>New Ed</Edition><ISBN>0306815435</ISBN><Label>Perseus Books Group</Label><ListPrice><Amount>1800</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$18.00</FormattedPrice></ListPrice><Manufacturer>Perseus Books Group</Manufacturer><NumberOfItems>1</NumberOfItems><NumberOfPages>480</NumberOfPages><ProductGroup>Book</ProductGroup><PublicationDate>2007-03-30</PublicationDate><Publisher>Perseus Books Group</Publisher><Studio>Perseus Books Group</Studio><Title>Tamerlane: Sword of Islam, Conqueror of the World</Title></ItemAttributes><OfferSummary><LowestNewPrice><Amount>1224</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$12.24</FormattedPrice></LowestNewPrice><TotalNew>1</TotalNew><TotalUsed>0</TotalUsed><TotalCollectible>0</TotalCollectible><TotalRefurbished>0</TotalRefurbished></OfferSummary></Item><Item><ASIN>1885221770</ASIN><DetailPageURL>http://www.amazon.com/gp/redirect.html%3FASIN=1885221770%26tag=ws%26lcode=sp1%26cID=2025%26ccmID=165953%26location=/o/ASIN/1885221770%253FSubscriptionId=0HP1WHME000749APYWR2</DetailPageURL><SalesRank>1135641</SalesRank><SmallImage><URL>http://ec1.images-amazon.com/images/P/1885221770.01._SCTHUMBZZZ_V1056534986_.jpg</URL><Height Units="pixels">60</Height><Width Units="pixels">40</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/1885221770.01._SCMZZZZZZZ_V1056534986_.jpg</URL><Height Units="pixels">140</Height><Width Units="pixels">93</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/1885221770.01._SCLZZZZZZZ_V1056534986_.jpg</URL><Height Units="pixels">475</Height><Width Units="pixels">317</Width></LargeImage><ImageSets><ImageSet Category="primary"><SmallImage><URL>http://ec1.images-amazon.com/images/P/1885221770.01._SCTHUMBZZZ_V1056534986_.jpg</URL><Height Units="pixels">60</Height><Width Units="pixels">40</Width></SmallImage><MediumImage><URL>http://ec1.images-amazon.com/images/P/1885221770.01._SCMZZZZZZZ_V1056534986_.jpg</URL><Height Units="pixels">140</Height><Width Units="pixels">93</Width></MediumImage><LargeImage><URL>http://ec1.images-amazon.com/images/P/1885221770.01._SCLZZZZZZZ_V1056534986_.jpg</URL><Height Units="pixels">475</Height><Width Units="pixels">317</Width></LargeImage></ImageSet></ImageSets><ItemAttributes><Author>Roy Stier</Author><Binding>Paperback</Binding><DeweyDecimalNumber>920</DeweyDecimalNumber><EAN>9781885221773</EAN><ISBN>1885221770</ISBN><Label>Bookpartners</Label><ListPrice><Amount>1695</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$16.95</FormattedPrice></ListPrice><Manufacturer>Bookpartners</Manufacturer><NumberOfItems>1</NumberOfItems><NumberOfPages>304</NumberOfPages><PackageDimensions><Height Units="hundredths-inches">79</Height><Length Units="hundredths-inches">900</Length><Weight Units="hundredths-pounds">92</Weight><Width Units="hundredths-inches">606</Width></PackageDimensions><ProductGroup>Book</ProductGroup><PublicationDate>1998-09</PublicationDate><Publisher>Bookpartners</Publisher><Studio>Bookpartners</Studio><Title>Tamerlane: The Ultimate Warrior</Title></ItemAttributes><OfferSummary><LowestUsedPrice><Amount>870</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$8.70</FormattedPrice></LowestUsedPrice><LowestCollectiblePrice><Amount>2295</Amount><CurrencyCode>USD</CurrencyCode><FormattedPrice>$22.95</FormattedPrice></LowestCollectiblePrice><TotalNew>0</TotalNew><TotalUsed>4</TotalUsed><TotalCollectible>1</TotalCollectible><TotalRefurbished>0</TotalRefurbished></OfferSummary><EditorialReviews><EditorialReview><Source>Book Description</Source><Content>From humble beginnings, Tamerlane, the ancient Turki-Mongol conqueror, rose to become the scourge of his time and changed the course of history.   &lt;P&gt;The name Tamerlane runs the gamut of human emotions, evoking in many a revulsion for the devil incarnate, in others, an appreciation for the benefactor of millions.   &lt;P&gt;By using accounts from Tamerlane's detractors and his admirers, Roy Stier has captured an amazing story that gives credence to the old adage, "truth is stranger than fiction."   &lt;P&gt;Tamerlane, the Ultimate Warrior is presented as a fascinating series of events and captures the reader in the first comprehensive view of this historical figure who dominated Asia and made Europe tremble.</Content></EditorialReview></EditorialReviews></Item></Items></ItemSearchResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>"""


if __name__ == '__main__':
    main()
