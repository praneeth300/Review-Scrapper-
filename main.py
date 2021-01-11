#import the libraries
from flask import Flask,render_template,request,jsonify

import requests
from bs4 import BeautifulSoup as bs

from urllib.request import urlopen as uReq
app=Flask(__name__) #intializing the flask app with a name 'app'

@app.route('/',methods=['GET'])
def homePage():
    return render_template('index.html')
@app.route('/scrap',methods=['POST']) #route with allowed method of POST and GET
def index():
    if request.method == 'POST':
        searchString=request.form['content'].replace(" ","") #Obtaining the search string entered in the form
        try:
            flipkart_url='https://www.flipkart.com/search?q='+searchString #preparing the url to search the string in the website
            uClient=uReq(flipkart_url) #Requesting the webpage from the internet
            flipkartPage=uClient.read() #Read the webpage
            uClient.close() #Close the connection from the webpage
            flipkart_html=bs(flipkartPage,"html.parser") #parsing the webpage as html
            bigboxes=flipkart_html.findAll("div", {'class': "_2pi5LC col-12-12"}) #Searching the apprpriate tag to ridirect the product link
            del bigboxes[0:3] #The first three members does'nt contain a relavent information hence we drop it
            box=bigboxes[0] #taking the first iteration for the demo
            productlink='https://www.filpkart.com'+box.div.div.div.a['href'] #Extracting the actual product link
            prodRes=requests.get(productlink) #getting the product page from the server
            prod_html=bs(prodRes.text,'html.parser') #parsing the product page html
            commentboxes=prod_html.findAll('div', {'class': '_16PBlm'}) #finding the html section containing customer comments

            reviews=[] #intializing the empty list for reviws
            for commentbox in commentboxes:
                try:
                    name=commentbox.div.div.find_all('p', {'class': '_2nMSwX _3oLIki'})[0].text
                except:
                    name='No name'
                try:
                    rating=commentbox.div.div.div.div.text
                except:
                    rating='No rating'
                try:
                    commentHead=commentbox.div.div.div.p.text
                except:
                    commentHead='No comment'
                try:
                    comtag=commentbox.div.div.find_all('div', {'class': ''})
                    custcomment=comtag[0].div.text
                except:
                    custcomment='No Customer comment'
                mydict={'Product': searchString, 'Name': name, 'Rating': rating, 'CommentHead': commentHead,
                        'Comment': custComment}

                reviews.append(mydict) #appending the results
            return render_template('results.html', reviews=reviews)
        except:
            return "Oops ! Something went wrong!!!!!!!!! Please check you entered detials are correct"

if __name__ == "__main__":
    app.run(debug=True, port=8000)