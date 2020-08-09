from rest_framework import renderers
import json

# this allows for intercepting the existing json Renderer and replacing its
# behavior to yours
class UserRenderer(renderers.JSONRenderer) :

    charset="utf-8"  # when you're creating a new renderer, you must specify this

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # if we want to change what the response will be 
        # update the data field

        if 'ErrorDetail' in str(data) :
            response = json.dumps({'errors' : data})
        else :
            response = json.dumps({'data': data})

        return response



    
