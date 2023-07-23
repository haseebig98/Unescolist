from django.shortcuts import render, get_object_or_404, redirect
from .models import Site, Fav, Comment
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from unesco.owner import OwnerDeleteView
from django.db import IntegrityError
from .forms import CommentForm

def sites_list(request):
    # Fetch the required fields for the first 20 sites from the database
    sites = Site.objects.all()[:20]

    strval =  request.GET.get("search", False)
    if strval :
            # Simple title-only search
        # __icontains for case-insensitive search
        query = Q(name__icontains=strval) | Q(description__icontains=strval) | Q(justification__icontains=strval) | Q(year__icontains=strval) | Q(tags__name__in=[strval])
        objects = Site.objects.filter(query).select_related().distinct().order_by('-year', 'category')[:10]
    else :
        objects = Site.objects.all().order_by('-year', 'category')[:10]


    return render(request, 'sites_list.html', {'sites' : objects, 'search': strval})


import requests

def get_image_url(site_name):
    api_key = 'AIzaSyDArecd2eVuLyjf9YM8JQyyyKsttYoBjiA'
    search_engine_id = '40a44d89d79eb4710'
    url = f'https://www.googleapis.com/customsearch/v1?q={site_name}&cx={search_engine_id}&searchType=image&key={api_key}'
    print("API Request URL:")
    print(url)

    try:

        response = requests.get(url)
        response_json = response.json()
        print("Got the response Hurraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaassssssssssssssssssssssssssah")
        print("Full API Response:")
        print(response_json)

        if 'items' in response_json:
            # Assuming the first image result is relevant
            first_image_result = response_json['items'][0]
            return first_image_result['link']

    except requests.RequestException as e:
        print(f"Error fetching image: {e}")

    return None






def site_detail(request, site_id):
    # Fetch the site based on the site_id
    site = get_object_or_404(Site, id=site_id)

    # Fetch image URL using the site name
    site_image_url = get_image_url(site.name)

    print(f"site_image_url: {site_image_url}")


    #Comments
    comments = Comment.objects.filter(site=site).order_by('-updated_at')
    comment_form = CommentForm()

    #Favorites
    favorites = []
    if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_sites.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]


    return render(request, 'site_detail.html', {'site': site, 'site_image_url': site_image_url, 'comments': comments, 'comment_form': comment_form, 'favorites': favorites})



class MyFavoritesView(LoginRequiredMixin, View):
    def get(self, request):
        user_favorites = Fav.objects.filter(user=request.user)
        favorite_sites = [fav.site for fav in user_favorites]
        return render(request, 'my_favorites.html', {'favorite_sites': favorite_sites})




class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, site_id) :
        f = get_object_or_404(Site, id=site_id)
        comment = Comment(text=request.POST['comment'], owner=request.user, site=f)
        comment.save()
        return redirect(reverse('unesco:site_detail', args=[site_id]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        site = self.object.site
        return reverse('unesco:site_detail', args=[site.id])






@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, site_id) :
        print("Add site_id",site_id)
        t = get_object_or_404(Site, id=site_id)
        fav = Fav(user=request.user, site=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, site_id) :
        print("Delete site_id",site_id)
        t = get_object_or_404(Site, id=site_id)
        try:
            Fav.objects.get(user=request.user, site=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
