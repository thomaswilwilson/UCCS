import re
import bs4
import queue
import json
import sys
import csv
import requests
import urllib3
from nltk.corpus import wordnet as wn, stopwords
import nltk
import collections
import normalize as n
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Queue:
    '''
    Queue that is used to hold all of the restaurant addresses
    '''
    def __init__(self):
        self.items = []
        self.all_items = set()

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)
        self.all_items.add(item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def go(Address=None):
    '''
    fucntion that fills the queue and then empties the queue. Analyzing the menu
    of each restaurant along the way

    input:
        Address: address that the user wants food delivered to

    outputs:
        rest_lst (list): list of restaurant dictionaries
        menu_lst (distionary): dictionary that holds all of the menu information
        keys are restaurants and the values are menu dictionaries
    '''
    rest_lst = []
    menu_lst = {}
    if Address:
        queue = queue_restaurants(Address)
    else:
        queue = queue_restaurants()
    while not queue.isEmpty():
        page = queue.dequeue()
        url = page[0] +'://' + page[1] + page[2]
        rest, menu = analyze_page(url)
        rest_lst.append(rest)
        menu_lst.update(menu)
    return rest_lst, menu_lst
        

def analyze_page(url):
    '''
    given a restraunt url from postmates, this function returns a dictionary
     containing information about the restaurant and a dictionary containing 
     information about the menu

    inputs:
        url (string): restaurant url
    
    outputs:
        rest (dictionary): dictionary containing restaurant name, address and 
        estimated delivery time
        final_menu (dictionary): dictionary containing menu item keys with 
         corresponding tuple values. The tuple contains three elements: the
         synset of the dish, the synset of the description and words in the 
         description aren't foods
    '''
    http = urllib3.PoolManager()
    urllib3.disable_warnings()
    request = http.request('GET', url)
    text = request.data
    soup = bs4.BeautifulSoup(text, features="lxml")
    rest = {}
    menu = {}
    final_menu = {}
    for script in soup.find_all('script', {'type': "application/ld+json"}):
        data = json.loads(script.text)

        if 'name' in data and 'address' in data and 'makesOffer' in data:

            rest['name'] = data['name']
            rest['streetAddress'] = data['address']['streetAddress']
            rest['state'] = data['address']['addressRegion']
            rest['postalCode'] = data['address']['postalCode']
            rest['minDeliveryTime'] = data['makesOffer']['deliveryLeadTime']['minValue']
            rest['maxDeliveryTime'] = data['makesOffer']['deliveryLeadTime']['maxValue']
            rest['logo'] = data['logo']['url']
            rest['header'] = data['image']['url']

        
        if "hasMenuSection" in data:
            del data['@id']
            del data['@type']
            del data['@reverse']
            del data['@context']

            for section in data['hasMenuSection']:

                if 'hasMenuItem' in section:
                    for food in section['hasMenuItem']:

                        food_name = food['name']
                        menu[food_name] = [None, None]
                        if 'description' in food:
                            menu[food_name][0] = food['description']
                        menu[food_name][1] = food['offers']['price']

            final_menu[rest['name']]= n.categorize(menu)
    
    return rest, final_menu


def queue_restaurants(Address=None):
    '''
    Given an adress, this function opens postmates.com and enters the address provided.
    Once the page is loaded with all restaurants that deliver to said address, 
    this function adds all urls of potential restaurants to a queue

    inputs:
        Adress (string): adress that the user wants to deliver to

    outputs:
        queue (class Queue): queue of all available restaurant urls
    '''
    queue = Queue()
    if Address:
        #gecko driver needs to be in the specified path. On the vm's our group had to change
        #student to whomevers ucid
        driver = webdriver.Firefox(executable_path=r'/home/student/cmsc-122-project/geckodriver.exe')
        driver.get('http://postmates.com')
        element = driver.find_element_by_id("e2e-geosuggest-input")
        element.send_keys(Address, Keys.ENTER)
        time.sleep(5)
        driver.get('http://postmates.com/feed')
        soup = bs4.BeautifulSoup(driver.page_source, "html5lib")
        driver.quit()

    else:
        soup = bs4.BeautifulSoup(html, "html5lib")

    match =[]
    for script in soup.find_all('script', {"type": "application/ld+json"}):

        match += re.findall('"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"', script.text)

    for url in match:

        if url[1] == "postmates.com" and re.findall('merchant', url[2]):
            queue.enqueue(url)

    return queue


html = '''
<!DOCTYPE html>
<html lang="">
<head>
<title>Food Delivery - Postmates On-Demand Delivery</title>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="dns-prefetch" href="https://raster-static.postmates.com">
<link rel="preconnect" href="https://raster-static.postmates.com">
<link rel="preload" href="https://buyer-static.postmates.com/dist/prod/vendors~client.c6d39df5a84ac5f4d660.js" as="script">
<link rel="preload" href="https://buyer-static.postmates.com/dist/prod/commons~admin~client.cb98308ae08fa77f79a4.js" as="script">
<link rel="preload" href="https://buyer-static.postmates.com/dist/prod/client.2ed8d02934b830e37cb9.js" as="script">
<meta name="description" content="Everyone&#39;s favorite delivery service! Lunch, dinner, groceries, office supplies or anything else. Our Postmates deliver from all your favorites places on-demand.">
<meta property="fb:app_id" content="378965782143277">
<meta name="msvalidate.01" content="80C2C8A14D93D9FE5C47205FC61FAB17">
<meta property="og:description" content="Everyone&#39;s favorite delivery service! Lunch, dinner, groceries, office supplies or anything else. Our Postmates deliver from all your favorites places on-demand.">
<meta property="og:image" content="https://buyer-static.postmates.com/dist/prod/postmates-share-image.9672924ea0390b5463f04664b04867d45837a47343a9a4a270746e3a4942cfa37d375ee60417eb26803966e4be663705fd86e7bdc1ff8e6c8a97a4f5bb30fa28.png">
<meta property="og:image:height" content="1200">
<meta property="og:image:width" content="1200">
<meta property="og:title" content="Food Delivery - Postmates On-Demand Delivery">
<meta property="og:type" content="website">
<meta name="twitter:app:id:googleplay" content="com.postmates.android">
<meta name="twitter:app:id:ipad" content="512393983">
<meta name="twitter:app:id:iphone" content="512393983">
<meta name="twitter:app:name:googleplay" content="Postmates">
<meta name="twitter:app:name:ipad" content="Postmates">
<meta name="twitter:app:name:iphone" content="Postmates">
<meta name="twitter:app:url:googleplay" content="postmates://">
<meta name="twitter:app:url:ipad" content="postmates://">
<meta name="twitter:app:url:iphone" content="postmates://">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:creator" content="@Postmates">
<meta name="twitter:description" content="Everyone&#39;s favorite delivery service! Lunch, dinner, groceries, office supplies or anything else. Our Postmates deliver from all your favorites places on-demand.">
<meta name="twitter:image" content="https://buyer-static.postmates.com/dist/prod/postmates-share-image.9672924ea0390b5463f04664b04867d45837a47343a9a4a270746e3a4942cfa37d375ee60417eb26803966e4be663705fd86e7bdc1ff8e6c8a97a4f5bb30fa28.png">
<meta name="twitter:site" content="@Postmates">
<meta name="twitter:title" content="Food Delivery - Postmates On-Demand Delivery">
<link rel="shortcut icon" href="https://buyer-static.postmates.com/dist/prod/favicon.f89de247941a7e54c249bcd265bdcf57ceb7cab7205f65d692ca90addf2115e2e2c9dfe5f9d7e4f97ca170c80098ab34d69264e0d11babc006684da9a849c0f0.ico">
<link rel="canonical" href="https://postmates.com/feed">
<link rel="dns-prefetch" href="//jssdkcdns.mparticle.com">
<link rel="preconnect" href="//jssdkcdns.mparticle.com">
<link rel="dns-prefetch" href="//cdn.ravenjs.com">
<link rel="preconnect" href="//cdn.ravenjs.com">
<link rel="dns-prefetch" href="//cdn.branch.io">
<link rel="preconnect" href="//cdn.branch.io">
<link rel="dns-prefetch" href="//connect.facebook.net">
<link rel="preconnect" href="//connect.facebook.net">
<link rel="dns-prefetch" href="//js.stripe.com">
<link rel="preconnect" href="//js.stripe.com">
<link rel="dns-prefetch" href="//maps.googleapis.com">
<link rel="preconnect" href="//maps.googleapis.com">
<link rel="dns-prefetch" href="//www.googletagmanager.com">
<link rel="preconnect" href="//www.googletagmanager.com">
<script type="text/javascript">
    (function (apiKey) {
      window.mParticle = window.mParticle || {};
      window.mParticle.eCommerce = { Cart: {} };
      window.mParticle.Identity = {};
      window.mParticle.config = window.mParticle.config || {};
      window.mParticle.config.isDevelopmentMode =  false ;
      window.mParticle.config.rq = [];
      window.mParticle.config.identifyRequest = {};
      window.mParticle.config.useCookieStorage = false;
      window.mParticle.ready = function(f) {
        window.mParticle.config.rq.push(f);
      };

       
       
      function a(o,t){
        return function(){t&&(o=t+"."+o);
          var e=Array.prototype.slice.call(arguments);
          e.unshift(o),
          window.mParticle.config.rq.push(e)
        }
      }
      var x=[
        "endSession",
        "logError",
        "logEvent",
        "logForm",
        "logLink",
        "logPageView",
        "setSessionAttribute",
        "setAppName",
        "setAppVersion",
        "setOptOut",
        "setPosition",
        "startNewSession",
        "startTrackingLocation",
        "stopTrackingLocation"
      ],
      y=["setCurrencyCode","logCheckout"],
      z=["login","logout","modify"];
      x.forEach(function(o){window.mParticle[o]=a(o)}),
      y.forEach(function(o){window.mParticle.eCommerce[o]=a(o,"eCommerce")}),
      z.forEach(function(o){window.mParticle.Identity[o]=a(o,"Identity")});

      var mp = document.createElement('script');
      mp.type = 'text/javascript';
      mp.async = true;
      mp.src = 'https://jssdkcdns.mparticle.com/js/v2/' + apiKey + '/mparticle.js';
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(mp, s);
    })("ae785bcecd586d4a89d0a2cd1cb96ce3");
  </script>
<script type="text/javascript">
   
   window.dataLayer = window.dataLayer || [];

   (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
   })(window, document,'script','dataLayer', "GTM-PXBWRF");
  </script>
<meta name="apple-mobile-web-app-title" content="Postmates On-Demand Delivery" /><meta name="apple-mobile-web-app-capable" content="yes" /><meta name="apple-mobile-web-app-status-bar-style" content="default" /><link rel="apple-touch-startup-image" href="https://buyer-static.postmates.com/dist/prod/icon_1024x1024.d760fcd9c5e149b12f7cb89e0bb80ef3.png" /><link rel="apple-touch-startup-image" href="https://buyer-static.postmates.com/dist/prod/icon_512x512.01ab01b568ce8dbe8ee3c82ebb52276b.png" /><link rel="apple-touch-icon" sizes="1024x1024" href="https://buyer-static.postmates.com/dist/prod/icon_1024x1024.d760fcd9c5e149b12f7cb89e0bb80ef3.png" /><link rel="apple-touch-icon" sizes="512x512" href="https://buyer-static.postmates.com/dist/prod/icon_512x512.01ab01b568ce8dbe8ee3c82ebb52276b.png" /><link rel="apple-touch-icon" sizes="384x384" href="https://buyer-static.postmates.com/dist/prod/icon_384x384.167be45577dd67231806d74792400838.png" /><link rel="apple-touch-icon" sizes="256x256" href="https://buyer-static.postmates.com/dist/prod/icon_256x256.34cb4c2e61f1b8f0b30256d1e2792a80.png" /><link rel="apple-touch-icon" sizes="192x192" href="https://buyer-static.postmates.com/dist/prod/icon_192x192.b65c9bd516227aa08b5879710bd44698.png" /><link rel="apple-touch-icon" sizes="128x128" href="https://buyer-static.postmates.com/dist/prod/icon_128x128.cfc5d33abed8a13c5d57c2d11552756e.png" /><link rel="apple-touch-icon" sizes="96x96" href="https://buyer-static.postmates.com/dist/prod/icon_96x96.e0fa112b22e822ac77e546e44d2eb216.png" /><link rel="manifest" href="https://buyer-static.postmates.com/dist/prod/manifest.d772bbebf1d4beb201f054e8c530a868.webmanifest" /></head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PXBWRF" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<script src="https://buyer-static.postmates.com/dist/prod/vendors~client.c6d39df5a84ac5f4d660.js" type="text/javascript" async></script>
<script src="https://buyer-static.postmates.com/dist/prod/commons~admin~client.cb98308ae08fa77f79a4.js" type="text/javascript" async></script>
<script src="https://buyer-static.postmates.com/dist/prod/client.2ed8d02934b830e37cb9.js" type="text/javascript" async></script>
<script type="application/ld+json">{"isPartOf":{"@id":"https://postmates.com#WebSite"},"@context":"https://schema.org","@id":"https://postmates.com/feed","@type":"WebPage","name":"Food Delivery - Postmates On-Demand Delivery","description":"Everyone's favorite delivery service! Lunch, dinner, groceries, office supplies or anything else. Our Postmates deliver from all your favorites places on-demand."}
</script><script type="application/ld+json">{"@type":"BreadcrumbList","@reverse":{"breadcrumb":{"@id":"https://postmates.com/feed"}},"itemListElement":[{"@type":"ListItem","position":1,"item":{"@id":"https://postmates.com","name":"Postmates On-Demand Delivery"}},{"item":{"@id":"https://postmates.com/feed","name":"Food Delivery - Postmates On-Demand Delivery"},"@type":"ListItem","position":2}],"@context":"https://schema.org","@id":"#BreadcrumbList"}
</script><script type="application/ld+json">{"numberOfItems":26,"itemListElement":[{"@type":"ListItem","position":1,"url":"https://postmates.com/merchant/subway-chicago-13"},{"@type":"ListItem","position":2,"url":"https://postmates.com/merchant/cafe-corea-chicago"},{"@type":"ListItem","position":3,"url":"https://postmates.com/merchant/cafe-53-chicago"},{"@type":"ListItem","position":4,"url":"https://postmates.com/merchant/saucy-porka-chicago-1"},{"url":"https://postmates.com/merchant/pho-55-chicago","@type":"ListItem","position":5},{"@type":"ListItem","position":6,"url":"https://postmates.com/merchant/checkers-chicago-5"},{"@type":"ListItem","position":7,"url":"https://postmates.com/merchant/maggies-gyros-chicago"},{"@type":"ListItem","position":8,"url":"https://postmates.com/merchant/nathans-chicago-style-1372-e-53rd-st"},{"@type":"ListItem","position":9,"url":"https://postmates.com/merchant/cedars-mediterranean-kitchen-chicago"},{"@type":"ListItem","position":10,"url":"https://postmates.com/merchant/jimmys-famous-burgers-chicago"},{"@type":"ListItem","position":11,"url":"https://postmates.com/merchant/fabianas-bakery-chicago"},{"position":12,"url":"https://postmates.com/merchant/new-grand-chinese-kitchen-chicago","@type":"ListItem"},{"@type":"ListItem","position":13,"url":"https://postmates.com/merchant/golden-fish-and-chicken-chicago"},{"@type":"ListItem","position":14,"url":"https://postmates.com/merchant/harolds-chicken-88-chicago"},{"@type":"ListItem","position":15,"url":"https://postmates.com/merchant/papa-johns-pizza-53rd-st-chicago"},{"@type":"ListItem","position":16,"url":"https://postmates.com/merchant/dunkin-donuts-chicago-1418-e-53rd-st"},{"@type":"ListItem","position":17,"url":"https://postmates.com/merchant/five-guys-burgers-and-fries-1456-e-53rd-st"},{"@type":"ListItem","position":18,"url":"https://postmates.com/merchant/potbelly-sandwich-shop-chicago"},{"@type":"ListItem","position":19,"url":"https://postmates.com/merchant/nella-pizza-e-pasta-chicago"},{"@type":"ListItem","position":20,"url":"https://postmates.com/merchant/starbucks-1174-e-55th-st"},{"position":21,"url":"https://postmates.com/merchant/baskinrobbins-chicago-1400-e-53rd-st","@type":"ListItem"},{"@type":"ListItem","position":22,"url":"https://postmates.com/merchant/nandos-periperi-chicago-1447-e-53rd-st"},{"@type":"ListItem","position":23,"url":"https://postmates.com/merchant/shinju-sushi-chicago"},{"url":"https://postmates.com/merchant/red-snapper-chicago-1418-e-53rd-st","@type":"ListItem","position":24},{"@type":"ListItem","position":25,"url":"https://postmates.com/merchant/porkchop-chicago"},{"@type":"ListItem","position":26,"url":"https://postmates.com/merchant/burger-king-chicago-52968"}],"@context":"https://schema.org","@id":"#MainEntityOfPage","@type":"ItemList","mainEntityOfPage":{"@id":"https://postmates.com/feed"},"name":"Food"}
</script>
<script type="text/javascript">!function(e){function a(a){for(var r,d,i=a[0],f=a[1],g=a[2],b=0,P=[];b<i.length;b++)d=i[b],c[d]&&P.push(c[d][0]),c[d]=0;for(r in f)Object.prototype.hasOwnProperty.call(f,r)&&(e[r]=f[r]);for(o&&o(a);P.length;)P.shift()();return n.push.apply(n,g||[]),t()}function t(){for(var e,a=0;a<n.length;a++){for(var t=n[a],r=!0,i=1;i<t.length;i++){var f=t[i];0!==c[f]&&(r=!1)}r&&(n.splice(a--,1),e=d(d.s=t[0]))}return e}var r={},c={61:0},n=[];function d(a){if(r[a])return r[a].exports;var t=r[a]={i:a,l:!1,exports:{}};return e[a].call(t.exports,t,t.exports,d),t.l=!0,t.exports}d.e=function(e){var a=[],t=c[e];if(0!==t)if(t)a.push(t[2]);else{var r=new Promise(function(a,r){t=c[e]=[a,r]});a.push(t[2]=r);var n,i=document.getElementsByTagName("head")[0],f=document.createElement("script");f.charset="utf-8",f.timeout=120,d.nc&&f.setAttribute("nonce",d.nc),f.src=function(e){return d.p+""+({0:"default~adawordsLandingPage~areaCategoryPage~areaPage~brandIndexPage~citiesPage~collectionPage~drink~8ccf6ac0",1:"default~areaCategoryPage~areaPage~citiesPage~collectionPage~drinksDeliveryPage~favoritesPage~feedPag~17aec187",2:"default~areaPage~checkoutPage~citiesPage~civicLabsPage~feedPage~foodFightPage~merchantPage~pressAndM~86e43bf4",3:"default~areaCategoryPage~areaPage~collectionPage~drinksDeliveryPage~feedPage~merchantPage~petsPage",4:"default~checkoutPage~giftcardPurchasePage~publicTrackingPage~settingsPage~trackingPage~unlimitedSign~b39519f9",5:"default~areaCategoryPage~checkoutPage~collectionPage~drinksDeliveryPage",6:"default~giftcardPurchasePage~unlimitedSignupPage~unlimitedSignupPageCapitalOne",7:"default~publicTrackingPage~trackingPage~trackingPageLite",8:"default~inTheNewsPage~pressAndMediaPage~pressReleasesPage",10:"default~publicTrackingPage~trackingPage",11:"default~adawordsLandingPage~landingPage",12:"default~civicLabsPage~foodFightPage",15:"intl",16:"areaPage",17:"areaCategoryPage",18:"authFormPage",19:"brandIndexPage",20:"brandMerchantPage",21:"brandOverviewPage",22:"checkoutPage",23:"citiesPage",24:"pickupNearMePage",25:"drinksLandingPage",26:"drinksDeliveryPage",27:"collectionPage",28:"eirPage",29:"favoritesPage",30:"feedPage",31:"giftcardPage",32:"giftcardPurchasePage",33:"intlLandingPage",34:"invitePage",35:"landingPage",36:"adawordsLandingPage",37:"legalPage",38:"merchantPage",39:"notificationsPage",40:"mobileMerchantLitePage",41:"orderHistoryPage",42:"petsPage",43:"pickupLandingPage",44:"publicTrackingPage",45:"referralPage",46:"searchPage",47:"settingsPage",48:"spotlightIndexPage",49:"spotlightPage",50:"aboutPage",51:"trackingPageLite",52:"unlimitedPage",53:"unlimitedPageCapitalOne",54:"unlimitedSignupPageCapitalOne",55:"foodFightPage",56:"pressAndMediaPage",57:"pressReleasesPage",58:"inTheNewsPage"}[e]||e)+"."+{0:"a619974c3ff24ca4b3c3",1:"834c66cf7cbaa30b3d6b",2:"30b8aae00be67e8a0bf5",3:"f0e2d0aba3d75552dbad",4:"2807864883800cba4484",5:"7bb4ede13ef5136981e6",6:"c0ff10fdfc2759cde308",7:"dd3b36783c524a57bbc5",8:"dd4125a840118aeef538",10:"b7010faf184c4fdcda38",11:"d7c38586bbf00be901ba",12:"a476ba84075df0fcfd94",15:"7732f0102b24059a4bbc",16:"bb9267b7a1adf53e9b0b",17:"b665b48553673b8532a1",18:"4128d415fe56d0197db7",19:"d9ffb52f35660ab2f1ed",20:"1fd543fbf5c22e2362ba",21:"15fbe14b92f9c2e3ffda",22:"d823c7972135ba048829",23:"8c062d39028a0db47fd5",24:"ec7d9ab9ed476a6d7b5a",25:"313a660f392c9464f491",26:"fdc12f3dfa02231b22b9",27:"71452e97b9b1e5e762c8",28:"016e0d6c4590e3c13c99",29:"c6bbfc6524c8f011dea6",30:"9b1feaccfd692b1d436a",31:"7f50ed4790264ef0715c",32:"e0f653768f0c00c244fb",33:"ee78aad29de2798414ba",34:"e062cf6b44ad940a2a1c",35:"86a76fb009ac5d13982a",36:"5df39cfcb44f1473864b",37:"d393896aac5b76c6c72f",38:"22875a9d583de3f75602",39:"e945bae9e16e4e184dbd",40:"c910a4925795d189f03f",41:"26e2a51c67b6f94d3a59",42:"4531167643e3e55d3347",43:"68c809b0b0e7266116ef",44:"518334a7e69edbf6141c",45:"4671e5a3354a312c4a48",46:"03f58d28e18e6217db08",47:"fd0ba7c79204f3c23bdf",48:"e93d1a078b1192b2fc50",49:"f6cc0f9c51d24eb6d345",50:"1dbf7af8f837a5ba12c5",51:"34e7ae363f3d2936ae50",52:"63c792852982f16b0b42",53:"a27e087757d9d0e660a3",54:"7c9e82ed15fcac9916b5",55:"4db1e79fef634ccf384d",56:"1aee34b2007e57a3efe9",57:"f6ce780c3809553a6ee3",58:"41046e836b1c7a92eb11"}[e]+".js"}(e),n=function(a){f.onerror=f.onload=null,clearTimeout(g);var t=c[e];if(0!==t){if(t){var r=a&&("load"===a.type?"missing":a.type),n=a&&a.target&&a.target.src,d=new Error("Loading chunk "+e+" failed.\n("+r+": "+n+")");d.type=r,d.request=n,t[1](d)}c[e]=void 0}};var g=setTimeout(function(){n({type:"timeout",target:f})},12e4);f.onerror=f.onload=n,i.appendChild(f)}return Promise.all(a)},d.m=e,d.c=r,d.d=function(e,a,t){d.o(e,a)||Object.defineProperty(e,a,{enumerable:!0,get:t})},d.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},d.t=function(e,a){if(1&a&&(e=d(e)),8&a)return e;if(4&a&&"object"==typeof e&&e&&e.__esModule)return e;var t=Object.create(null);if(d.r(t),Object.defineProperty(t,"default",{enumerable:!0,value:e}),2&a&&"string"!=typeof e)for(var r in e)d.d(t,r,function(a){return e[a]}.bind(null,r));return t},d.n=function(e){var a=e&&e.__esModule?function(){return e.default}:function(){return e};return d.d(a,"a",a),a},d.o=function(e,a){return Object.prototype.hasOwnProperty.call(e,a)},d.p="https://buyer-static.postmates.com/dist/prod/",d.oe=function(e){throw console.error(e),e};var i=window.webpackJsonp=window.webpackJsonp||[],f=i.push.bind(i);i.push=a,i=i.slice();for(var g=0;g<i.length;g++)a(i[g]);var o=f;t()}([]);
</script></body>
</html>

'''