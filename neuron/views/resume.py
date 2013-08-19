from pyramid.view import view_config
from neuron.utilities.authen import Authen
from neuron.utilities.register import RegisterUser
from neuron.utilities.prof_pic import ProfilePicture
from neuron.utilities.resume import Resume
from velruse import login_url
import json
import logging
import os

def resume_read(request):
    session=request.session
    uname=session['name']
    resobj=Resume(request)
    res_dic=resobj.resumeread(uname)
    return res_dic

def resume_write(request):
    setting=request.registry.settings
    session=request.session
    uname=session['name']
    collection_resume=request.db['resume']
    person=collection_resume.find_one({'username':uname})
    collection_schoolid=request.db['resume_misc']
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
    except KeyError:
        schools=[]
    no_of_p=request.params['p_tag']
    Address=request.params["address"]
    collection_school=request.db['school']
    for i in range(0,int(no_of_p)):
        flag=0
        sch=collection_schoolid.find_one({'name':'sid'})
        school_count=int(sch["value"])
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
            flag=1
        collection_school.update({'sid':schools[i]},{"$set":{'name':name[i],'date_of_joining':d_o_j[i],'date_of_leaving':d_o_l[i],'place':place[i],
        'marks_secured':m_s[i],'out_of':o_f[i]}},upsert=True)
        if(flag==1):
           collection_schoolid.update({'name':'sid'},{"$set":{'value':school_count+1}})
    collection_resume.update({'username':uname},{"$set":{'address':Address,'school':schools}},upsert=True)
    colleges=[]
    degree=[]
    course=[]
    name_coll=[]
    place_coll=[]
    d_o_j_coll=[]
    d_o_l_coll=[]
    project_ids=[]
    m_s_coll=[]
    o_f_coll=[]
    no_of_pc=0  #college_p_tag
    try:
        colleges=person['college']
    except KeyError:
        colleges=[]
    except TypeError:
        colleges=[]
    no_of_pc=request.params['no_of_pc']
    collection_college=request.db['graduate']
    for i in range(0,int(no_of_pc)):
        flag=0
        cch=collection_schoolid.find_one({'name':'cid'})
        college_count=int(cch["value"])
        if not college_count:
            college_count=0
        degree.append(request.params['degree_college_'+str(i)])
        course.append(request.params['course_college_'+str(i)])
        name_coll.append(request.params['name_college_'+str(i)])
        place_coll.append(request.params['city_college_'+str(i)])
        d_o_j_coll.append(request.params['doj_college_'+str(i)])
        d_o_l_coll.append(request.params['dol_college_'+str(i)])
        m_s_coll.append(request.params['ms_college_'+str(i)])
        o_f_coll.append(request.params['outof_college_'+str(i)]) 
        try: 
            temp=colleges[i]
        except IndexError:
            colleges.append(college_count+1)
            flag=1
        collection_college.update({'gid':colleges[i]},{"$set":{'degree':degree[i],'course':course[i],'name':name_coll[i],'date_of_joining':d_o_j_coll[i],'date_of_leaving':d_o_l_coll[i],'place':place_coll[i],'marks_secured':m_s_coll[i],'out_of':o_f_coll[i]}},upsert=True)
        if(flag==1):
           collection_schoolid.update({'name':'cid'},{"$set":{'value':college_count+1}})
    collection_resume.update({'username':uname},{"$set":{'address':Address,'college':colleges}},upsert=True)   
    return {'address':Address,'username':uname,'no_of_p':no_of_p,'name':name,'d_o_j':d_o_j,'d_o_l':d_o_l,'place':place,'m_s':m_s,'o_f':o_f,
    'no_of_pc':no_of_pc,'degree':degree,'course':course,'name_coll':name_coll,'place_coll':place_coll,'d_o_j_coll':d_o_j_coll,'d_o_l_coll':d_o_l_coll,
    'm_s_coll':m_s_coll,'o_f_coll':o_f_coll}
    
def resume_delete(request):
    setting=request.registry.settings
    session=request.session
    uname=session['name']
    collection_resume=request.db['resume']
    collection_school=request.db['school']
    collection_college=request.db['graduate']
    person=collection_resume.find_one({'username':uname})
    d=request.params["del"]
    d=d.split("_")
    #print d[0],d[1]
    val=d[0]
    no=int(d[1])
    if(val=="sch"):
         school=person["school"]
         #print school
         sc=school[no]
         del school[no]
         #print school
         collection_resume.update({'username':uname},{"$set":{'school':school}})
         collection_school.remove({'sid':sc})
    if(val=="cch"):
        college=person["college"]
        cc=college[no]
        del college[no]
        collection_resume.update({'username':uname},{"$set":{'college':college}})
        collection_college.remove({'gid':cc})
    resobj=Resume(request)
    res_dic=resobj.resumeread(uname)
    return res_dic

