from random import choice, randint
import Image, ImageDraw, ImageFont, sha
#from decapole.settings import MEDIA_ROOT, SECRET_KEY
from settings import MEDIA_ROOT, SECRET_KEY
#from PIL import Image, ImageDraw

class Captcha:
   
    def gerarImagem(self, ipAddress):
        
        num_numbers = randint(1, 4)
        num_letters = 5 - num_numbers
#        tipo_validacao = randint(0,1)
#        pergunta=""
       
        imgtextL = ''.join([choice('QWERTYUOPASDFGHJKLZXCVBNM') for i in range(num_letters)])
        imgtextN = ''.join([choice('123456789') for i in range(num_numbers)])

        SALT = SECRET_KEY[:20]
        imgtext = ''.join([choice(imgtextL + imgtextN) for i in range(5)])

        print '----------------------------------------'
        print 'imgtext ' + imgtext
        
        im = Image.open(MEDIA_ROOT + '/imagens/captcha.jpg')
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(MEDIA_ROOT + '/fonts/captcha.ttf', 30)
        draw.text((28,10),imgtext, font=font, fill=(255))
        
        temp = MEDIA_ROOT + "/imagens/temp/" + ipAddress + '.jpg'
        tempname = ipAddress + '.jpg'
        im.save(temp, "JPEG")
        
        imghash = sha.new(SALT+imgtext).hexdigest()
        
        return {'captcha_img_name':tempname, 'hash_code_captcha':imghash}
 
