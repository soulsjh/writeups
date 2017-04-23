import random
from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.PublicKey import RSA

def get_rand_bytes(length):
  return "".join([chr(random.randrange(256)) for i in range(length)])

def encrypt(public_key, message):
  """Encrypt a message with a given public key.

  Takes in a public_key generated by Crypto.PublicKey.RSA, which must be of
  size exactly 4096
  """
  symmetric_key = get_rand_bytes(32)
  msg_header = PKCS1_OAEP.new(public_key).encrypt(symmetric_key)
  assert len(msg_header) == 512
  msg_iv = get_rand_bytes(16)
  msg_body = AES.new(symmetric_key,
      mode=AES.MODE_CFB,
      IV=msg_iv).encrypt(message)
  return msg_header + msg_iv + msg_body

def decrypt(private_key, ciphertext):
  """Decrypt a message with a given private key.

  Takes in a private_key generated by Crypto.PublicKey.RSA, which must be of
  size exactly 4096

  If the ciphertext is invalid, return None
  """
  if len(ciphertext) < 512 + 16:
    return None
  msg_header = ciphertext[:512]
  msg_iv = ciphertext[512:512+16]
  msg_body = ciphertext[512+16:]
  try:
    symmetric_key = PKCS1_OAEP.new(private_key).decrypt(msg_header)
  except ValueError:
    return None
  if len(symmetric_key) != 32:
    return None
  return AES.new(symmetric_key,
      mode=AES.MODE_CFB,
      IV=msg_iv).decrypt(msg_body)


if __name__=="__main__":
  # Test!
  message = "This is my test message.  It's kind of ssilly.wireheirhgwieruhgwieurghwiregsilly.wireheirhgwieruhgwieurghwiregsilly.wireheirhgwieruhgwieurghwiregsilly.wireheirhgwieruhgwieurghwiregsilly.wireheirhgwieruhgwieurghwiregsilly.wireheirhgwieruhgwieurghwiregsilly.wireheirhgwieruhgwieurghwiregsilly.wireheirhgwieruhgwieurghwiregsilly.wireheirhgwieruhgwieurghwiregsilly.wireheirhgwieruhgwieurghwiregsilly.wireheirhgwieruhgwieurghwiregilly.wireheirhgwieruhgwieurghwireg"
  f = open('ciphertext-2.bin', 'r')
  message = f.read()
  n = 549100898763808112064590568096509639806005267015788479836998648112330729762142760306265813195181231930171220686827142359040315653020182064933039077953579528749272321744478656324986362155106653831095037724728643255316641716947998245610175805278242802144980117927688674393383290354985820646326870614197414534217177211618710501438340081867982883181358830449072661742417246835970022211465130756382481343160426921258769780282358703413114522476037306476452786236456339806564839822630841425055758411765631749632457527073092742671445828538125416154242015006557099276782924659662805070769995499831691512789480191593818008294274869515824359702140052678892212293539574359134092465336347101950176544334845468112561615253963771393076343090247719105323352711194948081670662350809687853687199699436636944300210595489981211181100443706510898137733979941302306471697516217631493070094434891637922047009630278889176140288479340611479190580909389486067761958499091506601085734094801729179308537628951345012578144960250844126260353636619225347430788141190654302935255862518781845236444151680147886477815759103864509989480675169631226254252762579781553994364555800120817100328166428687776427164098803076677481602221304265962340500651339469391627432175447
  d = 82360526616896807698693573199664438409937065969470070589061697203467920610817023646959077756968989532459091749350432099444980199654188634836861161137356662441445859352927217157270793987104238155332957760232748731947002017400746597944533389986864375329359088386551101208283522331411651732989376273218842814180319110433001694202809406529081151328224220501000292507144740713386831323918799559242796888829373272839049340208231242397384963518461448183826706394044211875954303427851825251639033541902213506905901969121366029468891668656797568632939181423824723939930127468565302483191827000307215869460583072592787394379648492838431373480501883096871724639329379422198017519406310001449118250257352155151242793946860974388275256551958325634162505006352633974367733621639608704430697868358325477517705349062070604806141047285976585695001741441171974331457858532665535006295162620342801636572553939160973573287838150248262669409134863998676177317567799700878113228884526337190956961963516058441888168118633266674943833985047193671213626257221952126625834587189721310168003199270210218744859703599407641156335251120773805978641928778006104069967130056321615203155638339974487535580497188409267435564860804781546983286452847097738671150588113
  e = 65537L
  p = 2758599203L
  q = 199050626189790903113151725251371951406311367304411013359159100762029303668345459282823483508119186508070350039475140948570888009866572148405365532164833126992414461936781273087675274788769905198546175946505790118332257676994622928414648644875376193656132263418075334807302665038501361680530751104620475935886499714767992159620130246904875540624651891646715835632182355428589610236128648209568297096024509697960196858754170641081387466229916585122877955908862176165344465889280850859817985096316883025515924332365977538735425288433292357532172467247159245727072344354499113900733623716569924461327947462469348798798400461045817375922057805611166274339541877392159201774893120311667898551312256530117094221191204981071357303328506659872809131929265966688409379037586014938643190675726674943253875287765020503118408406103824607730713529079962656130622218633922911733000466212212532871890933508287965723844399784165195088175666883742686183165151553009638524764735387233844317375317153437534933611361683136151569588355535831475925641431859231311079029505004457816932257031352498323214304125608733640306746900473758755832661915903475867854937735150255829715879232213599597863424779218670961633567259935246911742292942052832671549L
  private_key = RSA.construct((n, e, d, p, q))
  plaintext = decrypt(private_key, message)
  print(plaintext)
  # private_key = RSA.generate(4096)
  # public_key = private_key.publickey()
  # RSA.construct()
  # ciphertext = encrypt(public_key, message)
  # assert message == decrypt(private_key, ciphertext)
