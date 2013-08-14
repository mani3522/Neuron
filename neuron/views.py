from pyramid.view import view_config
from login.authen import Authen
from login.register import RegisterUser
from login.prof_pic import ProfilePicture
from velruse import login_url
import json
import logging
import os
#@view_config(route_name='home', renderer='login:templates/index.pt')
def index(request):
    return {'page':'login', 'state':'Please SIGN IN !!!'}

#@view_config(route_name='auth', renderer='login:templates/auth.pt')
def authenticate(request):
    username=request.params["uname"]
    password=request.params["pword"]
    Userdata=Authen(request)
    session=request.session
    if(Userdata.CheckUser(username,password)):
       session['name']=username
       session.save()
       return {'username':username, 'password':password, 'state': 'successful','session':session['name']}
    else:
        session.invalidate()
        return {'username':username, 'password':password, 'state': 'try again','session':'empty'}

def session_check(request):
    session=request.session
    return {'session':session['name']}

def register_profiledetails(request):
    session=request.session
    fname=request.params["fname"]
    lname=request.params["lname"]
    date=request.params["date"]
    month=request.params["month"]
    year=request.params["year"]
    city=request.params["ccity"]
    designation=request.params["designation"]
    print(session['name'],fname,lname,date,month,year,city,designation)
    return {'username':'appu', 'password':'appu', 'state': 'successful'}

def signup(request):
    return { 'page': 'SIGN UP!!!!'}

def register_user(request):
    username=request.params["uname"]
    password=request.params["pword"]
    email=request.params["email"]
    WriteUser= RegisterUser(request)
    WriteUser.EnterUser(username,password,email)
    session=request.session
    session['name']=username
    session.save()
    return {'username':username, 'password':password, 'state': 'successful'}

def login_view(request):
    return {
        'login_url': login_url,
        'providers': request.registry.settings['login_providers'],
    }

def process_profile_picture(request):
    input_file=request.POST["prof_pic"].file
    project_home=os.environ['PROJECT_HOME']
    tmp=project_home+"/login/static/images/"
    session=request.session
    username=session['name']
    tmp = tmp + username
    if not os.path.exists(tmp):
        os.makedirs(tmp)
    tmp= tmp + "/img0.jpeg"
    output=open(tmp, 'w')
    output.write(input_file.read())
    output.close()
    ppobj=ProfilePicture(request)
    ppobj.EnterFirstProfPic(username)
    return { 'username':username, 'password':'password', 'state':'saved','session':session['name']}

def resume_read(request):
    setting=request.registry.settings
    session=request.session
    uname=session['name']
    collection=request.db['resume']
    Resume=collection.find_one({'username':uname})
    #check_address=Resume.get('address',None)
    try:
        Address=Resume['address']
    except TypeError:
        Address='Enter your address'
    schools=[]
    name=[]
    d_o_j=[]
    d_o_l=[]
    place=[]
    m_s=[]
    o_f=[]
    no_of_p=0
    try:
        schools=Resume['school']
    except TypeError:
        schools=[]
    i=0
    for school in schools:
        collection_school=request.db['school']
        school_detail=collection_school.find_one({'sid':school})
        name.append(school_detail['name'])
        d_o_j.append(school_detail['date_of_joining'])
        d_o_l.append(school_detail['date_of_leaving'])
        place.append(school_detail['place'])
        m_s.append(school_detail['marks_secured'])
        o_f.append(school_detail['out_of'])
        i=i+1
        no_of_p=i;
    return {'address':Address,'username':uname,'no_of_p':no_of_p,'name':name,'d_o_j':d_o_j,'d_o_l':d_o_l,'place':place,'m_s':m_s,'o_f':o_f}
    
def resume_write(request):
    setting=request.registry.settings
    session=request.session
    uname=session['name']
    collection_resume=request.db['resume']
    person=collection_resume.find_one({'username':uname})
    schools=[]
    name=[]
    d_o_j=[]
    d_o_l=[]
    place=[]
    m_s=[]
    o_f=[]
    try:
        schools=person['school']
    except TypeError:
        schools=[]
    no_of_p=request.params['p_tag']
    #print no_of_p
    Address=request.params["address"]
    collection_school=request.db['school']
    for i in range(0,int(no_of_p)):
        school_count=collection_school.count()
        if not school_count:
            school_count=0
        name.append(request.params['name_school_'+str(i)])
        d_o_j.append(request.params['doj_school_'+str(i)])
        d_o_l.append(request.params['dol_school_'+str(i)])
        place.append(request.params['city_school_'+str(i)])
        m_s.append(request.params['ms_school_'+str(i)])
        o_f.append(request.params['outof_school_'+str(i)])
        try: 
            temp=schools[i]
        except IndexError:
            schools.append(school_count+1)
        collection_school.update({'sid':schools[i]},{"$set":{'name':name[i],'date_of_joining':d_o_j[i],'date_of_leaving':d_o_l[i],'place':place[i],
        'marks_secured':m_s[i],'out_of':o_f[i]}},upsert=True)
    collection_resume.update({'username':uname},{"$set":{'address':Address,'school':schools}},upsert=True)
    return {'address':Address,'username':uname,'no_of_p':no_of_p,'name':name,'d_o_j':d_o_j,'d_o_l':d_o_l,'place':place,'m_s':m_s,'o_f':o_f}
    

def login_complete_view(request):
    context = request.context
    result = {
        'profile': context.profile,
        'credentials': context.credentials,
    }
    #print(result['profile']['accounts'])
    account=result['profile']['accounts']
    domain=account[0]['domain']
    if(domain=="facebook.com"):
        username=result['profile']['preferredUsername']
        setting = request.registry.settings
        collection = request.db['users']
        flag_to_insert=collection.find_one({'username':username})
        if not flag_to_insert:
            user={'username':username, 'email_id':result['profile']['verifiedEmail']}
            collection.insert(user)
    if(domain=="twitter.com"):
        username=result['profile']['displayName']
        setting = request.registry.settings
        collection = request.db['users']
        flag_to_insert=collection.find_one({'username':username})
        if not flag_to_insert:
            user={'username':username}
            collection.insert(user)
        
   #print(result['profile']['displayName'])
    return {
        'result': json.dumps(result, indent=4)
    }
