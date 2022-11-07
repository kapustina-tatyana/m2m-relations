from django.views.generic import ListView
from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'
    articles = Article.objects.order_by(ordering).prefetch_related('section').values('id', 'title', 'image', 'text', 'section__name', 'relationship__main_section')

    object_list = []
    articles_counter = []
    for article in articles:
        if article['id'] not in articles_counter:
            articles_counter.append(article['id'])
            a_object = {}
            a_object['id'] = article['id']
            a_object['title'] = article['title']
            a_object['image'] = article['image']
            a_object['text'] = article['text']
            a_object['scopes'] = {'all':[{'tag': {'name': article['section__name']}, 'is_main': article['relationship__main_section']}]}
            object_list.append(a_object)
        else:
            for o_list in object_list:
                if o_list['id'] == article['id']:
                    o_list['scopes']['all'].append({'tag': {'name': article['section__name']}, 'is_main': article['relationship__main_section']})

    context = {
        'object_list': object_list
    }



    return render(request, template, context)
