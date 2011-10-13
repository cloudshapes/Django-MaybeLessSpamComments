from django.contrib.comments.views.comments import post_comment
from django.http import HttpResponseRedirect

def maybelessspamcomment_post_comment(request):
        if 'url' in request.REQUEST and 'preview' not in request.REQUEST:
                response = post_comment(request)
            
                # Check there's a url to redirect to, and that post_free_comment worked
		redirect_url = request.REQUEST['redirect_url']
                if len(redirect_url.strip()) > 0 and isinstance(response, HttpResponseRedirect):
                        return HttpResponseRedirect(redirect_url)
                
                # Fall back on the default post_free_comment response
                return response
        
        return post_comment(request)

