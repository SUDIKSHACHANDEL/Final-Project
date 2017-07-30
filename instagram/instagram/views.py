# _*_ coding: utf-8 _*_
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from datetime import datetime
from demoapp.forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from django.contrib.auth.hashers import make_password, check_password
from demoapp.models import UserModel, SessionToken, PostModel, LikeModel, CommentModel
from datetime import timedelta
from django.utils import timezone
from instagram.settings import BASE_DIR
from imgurpython import ImgurClient
from django.http import HttpResponse
# from clarifai.rest import ClarifaiApp
# from clarifai.rest import Image as ClImage
# from enum import Enum






client_id='f9dc99672fce970'
client_secret='adac019ab6a9a2114e85c9c2e7829eb38a8b5d'
#


def signup_view(request):
    dict={}
    if request.method == 'GET':
        signup_form = SignUpForm()                             # calling & display signup form
        template_name = 'signup.html'                          # rendering to signup.html after get reqst

    elif request.method == 'POST':
        signup_form = SignUpForm(request.POST)                 # calling & process the form data
        if signup_form.is_valid():                             # validate the form data
            username = signup_form.cleaned_data['username']
            name     = signup_form.cleaned_data['name']
            email    = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            while len(username) < 4:
                dict['invalid_username']="Usename must be atleast 5 characters"
                return render(request, "signup.html",dict)
            while len(password) < 5:
                dict['invalid_password']="Password must be at least 5 characters"
                return render(request, "signup.html",dict)

            new_user = UserModel(name=name, email=email, password=make_password(password), username=username)
            new_user.save()                                    # save data to db
            template_name = 'success.html'                     # rendering to success.html after post req
        else:
            dict={"key":"Pleas fill the form"}
            return render(request,'signup.html',dict)

    return render(request,template_name, {'signup_form': signup_form})

def login_view(request):
    response_data = {}
    # if request.method == 'GET':
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #validation successful
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            #read data from db
            user = UserModel.objects.filter(username=username).first()
            if user:
                #compare password
                if check_password(password, user.password):
                    token = SessionToken(user=user)       #if password matches session token generaed
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    return render(request,'login_fail.html')
            else:
                return render(request, 'login_fail.html')
        else:
            return HttpResponse("Invalid form data.")
    elif request.method == 'GET':
        form = LoginForm()
        response_data['form'] = form

    return render(request, 'login.html', response_data)

def check_user(request):
    if request.COOKIES.get("session_token"):
        session = SessionToken.objects.filter(session_token = request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
        else:
            return None

def feed_view(request):
    user = check_user(request)
    if user and request.method == 'GET':
        posts = PostModel.objects.all().order_by('-created_on')
        for post in posts:
            existing_like = LikeModel.objects.filter(post = post.id,user = user)
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'posts': posts})
        # elif user and request.method== 'POST':

def post_view(request):
    user = check_user(request)
    if user == None:
        return redirect('/login/')
    elif request.method == 'GET':
        post_form = PostForm()
        return render(request, 'post.html', {'post_form': post_form})
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            post = PostModel(user=user, image=image, caption=caption)
            post.save()
            client = ImgurClient('f9dc99672fce970','adac0c019ab6a9a2114e85c9c2e7829eb38a8b5d')
            path = str(BASE_DIR + "\\" +  post.image.url)
            post.image_url = client.upload_from_path(path,anon=True)['link']
            post.save()
            # app = ClarifaiApp()
            # app.tag_urls(urls=['https://samples.clarifai.com/wedding.jpg'], model='food-items-v1.0')

            return redirect("/feed/")
        else:
            return HttpResponse("Form data is not valid.")
    else:
        return HttpResponse("Invalid request.")
def like_view(request):
    user = check_user(request)
    if user and request.method == 'POST':
        #HttpResponse("form data is not valid")

        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
        else:
            HttpResponse("form data is not valid")
    else:
        return redirect('/login/')
def comment_view(request):
    user = check_user(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            current_post = PostModel.objects.filter(id=post_id).first()
            comment = CommentModel.objects.create(user=user, post=current_post, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')


def logout_view(request):
    user_id = check_user(request)
    delete_user = SessionToken.objects.filter(user = user_id)
    delete_user.delete()
    return redirect('/login/')


# directory = expanduser('~/pictures/clarifai/')
# pictures = ['images (3).jpg', 'images (3).jpg']
#
# clarifai_api = ClarifaiApi()
# results = clarifai_api.tag_images(
#     [open('%s%s' % (directory, p), 'rb') for p in pictures]
# )
#
# # Uncomment the below to print the whole JSON returned
# # from pprint import pprint
# # pprint(result)
#
# for i, result in enumerate(results['results']):
#     tags = result['result']['tag']
#     print '\nTags for %s (Tag - Probability)' % pictures[i]
#     for j in range(len(tags['classes'])):
#         print '%s - %0.4f' % (tags['classes'][j], tags['probs'][j])
#
API_KEY="e6e4f369d43746e0aac1f5794d35d32e"

# def add_category(post):
#     app = ClarifaiApp(api_key='{e6e4f369d43746e0aac1f5794d35d32e}')
#     model = app.models.get("general-v1.3")
#     response = model.predict_by_url(url=post.image_url)
#
#     if response["status"]["code"] == 10000:
#         if response["outputs"]:
#             if response["outputs"][0]["data"]:
#                 if response["outputs"][0]["data"]["concepts"]:
#
#
#                     for index in range(0,len(response["outputs"][0]["data"]["concepts"])):
#                         category=ClImage(post=post,category_text=response["outputs"][0]["data"]["concepts"][index]["name"])
#                         category.save()
#                 else:
#                     print "No concepts List Error"
#             else:
#                 print"No data list error"
#         else:
#             print("No Output list error")
#     else:
#         print"Response code Error"