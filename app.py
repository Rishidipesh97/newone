from flask import flash,redirect,render_template,request,session,url_for,send_from_directory

from forms import institute_update_form,authentications,personal_update_form
import mysql.connector
import pandas as pd
from datetime import datetime
import numpy as np
import csv
import os


app= Flash(__name__)

# mydb=mysql.connector.connect(host='localhost',user='root',passwd='1234',database='ridham')
# mycursor = mydb.cursor(buffered=True)

# mydb2=mysql.connector.connect(host='localhost',user='root',passwd='1234',database='ridham_2')
# mycursor2 = mydb2.cursor(buffered=True)


mydb=mysql.connector.connect(host='remotemysql.com',user='7SfpY1qGtT',passwd='Tv7OfgemPh',database='7SfpY1qGtT')
mycursor = mydb.cursor(buffered=True)

mydb2=mysql.connector.connect(host='remotemysql.com',user='cVTsksiGpK',passwd='5lxL6XRUOE',database='cVTsksiGpK')
mycursor2 = mydb2.cursor(buffered=True)

 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route('/')
def index99():
   
   return ("Welcome")

@app.route('/admin')
def index():
   lf=authentications()
   return render_template('authentication.html',lf=lf)



@app.route('/authentication.py')
def index1():
   # scheduler = apscheduler.schedulers.blocking.BackgroundScheduler('apscheduler.job_defaults.max_instances': '2')
   name=request.values.get('name')
   passw=request.values.get('password')

   if str(name)=='drivekraft' and str(passw)=='elon':
      return render_template('front_pg_admin.html')
   else:
      return('some thing is worng')



@app.route('/front_pg_admin.html')
def index2():
   return render_template('front_pg_admin.html')




@app.route('/update_institute.html')
def index3():
   lf=institute_update_form()
   return render_template('update_institute.html',lf=lf)


@app.route('/update_institute.py')
def index4():
    identity=request.values.get('identity')
    i_name=request.values.get('Institute_name')
    address=request.values.get('address')
    contact=request.values.get('contact') 

    sql="insert into institute(i_id,name,address,contact) values(%s,%s,%s,%s)"
    val =(identity,i_name,address,contact) 
        
    mycursor.execute(sql, val)  
    mydb.commit()
    return ("done")   



@app.route('/update_teacher.html')
def index5():
   pf=personal_update_form()
   return render_template('update_teacher.html',pf=pf)



@app.route('/update_teacher.py')  
def index6():
  id_institute=request.values.get('id_institute')
  file_name=request.values.get('file_name') 

  dataset=pd.read_csv(str(file_name))
  credentilals=dataset[:].values

  for i in credentilals:
          sql="insert into teacher(name,i_id) values(%s,%s)"
          val =(i[0],id_institute)
          mycursor = mydb.cursor()
          mycursor.execute(sql, val)
          mydb.commit()

  return('done')        




@app.route('/update_student.html')
def index7():
  pf=personal_update_form()
  return render_template('update_student.html',pf=pf)


@app.route('/update_student.py')
def index8():
  standard=request.values.get('standard')
  id_institute=request.values.get('id_institute')
  batch=request.values.get('batch')
  file_name=request.values.get('file_name')

  dataset=pd.read_csv(str(file_name))
  credentilals=dataset[:].values

  for i in credentilals:
          sql="insert into student(name,standard,batch,institute_personal_id,email,contact,i_id) values(%s,%s,%s,%s,%s,%s,%s)"
          val =(i[1],standard,batch,i[0],i[2],i[3],id_institute)
          print(i[1])

          mycursor = mydb.cursor()
          mycursor.execute(sql, val)
          mydb.commit()


          sql="insert into rel_student_institute(i_id,s_id) values(" + str(id_institute)  + " , (select s_id from student where institute_personal_id = " + str(i[0]) + " and i_id = " + str(id_institute) + ") )"
          

          mycursor = mydb.cursor()
          mycursor.execute(sql)
          mydb.commit()

  return ("done")   





@app.route('/teacher/<id1>')
def index9(id1):
   session['check_it']='PASS_word'
   session['t_id']=str(id1)

   sql="select i_id from teacher where t_id =" + str(id1)
   mycursor.execute(sql)
   result=mycursor.fetchone()
   session['i_id'] =str(result[0])

   return render_template('teacher_initiaal_template.html')



@app.route('/make_test.html')
def index10():

   if(session.get('check_it')==None):
     return render_template('error_404_1.html')


   session['j']=0
   return render_template('make_test1.html')


@app.route('/date_number.py')
def index11():

   if(session.get('check_it')==None):
     return render_template('error_404_1.html')



   date=request.values.get('date')
   ques=request.values.get('ques')

   session['date']=date
   session['ques']=ques

   return render_template('make_test2.html')


@app.route('/time_time.py')
def index12():

   if(session.get('check_it')==None):
     return render_template('error_404_1.html')


   stime=request.values.get('starting_time')
   etime=request.values.get('ending_time')

   sql="insert into exam(s_time,e_time,date,active) values('" + str(stime) +"','" + str(etime) + "','" + str(session['date']) + "'," + "0)";
   mycursor.execute(sql)
   mydb.commit()

   mycursor2.execute(sql)
   mydb2.commit()

   sql= "select * from exam"
   mycursor.execute(sql)
   result=mycursor.fetchall()

   test_id= result[-1][0]
   session['exam_id']=test_id

   sql= "insert into rel_institute_exam values(" + str(test_id) + ","+ str(session['t_id']) + "," + "NULL)";
   mycursor.execute(sql)
   mydb.commit()

   le = session['ques']
   return render_template('make_batch.html')


@app.route('/batch.py')
def index13():

   if(session.get('check_it')==None):
     return render_template('error_404_1.html')


   batch=request.values.get('batches')
   you=batch.split(',') 

   ki=''
   for i in you:
    ki= ki+  str(i) 
    if str(i) in you[:-1]:
      ki= ki + ","

   sql="update rel_institute_exam set batches=  '" + str(ki) +"' where e_id ='" + str(session['exam_id']) + "'"
   mycursor.execute(sql)
   mydb.commit()

   return render_template('make_test3.html',le=str(session['ques']),test_id=session['exam_id'])


@app.route('/es.html',methods=["POST"])
def index14():
  target=os.path.join(APP_ROOT,'images/')
  print(target)

  if not os.path.isdir(target):
    os.mkdir(target)


  if(session.get('check_it')==None):
     return render_template('error_404_1.html')


  # j=0
  # for file in request.files.getlist("picq"):
  #     filename=file.name + str(j) + ".png"
  #     j=j+1
  #     destination= "/".join([target,filename])
  #     print(destination)
  #     file.save(destination)  

  
  final=request.values.get('final')
  detail=list();
  detail=final.split('//')
   
  for i in detail[:-1]: 
       esh=i.split('@')
       ques_no=str(esh[0])
       ques=esh[1]
       oa=esh[2]
       ob=esh[3]
       oc=esh[4]
       od=esh[5]
       corr=esh[6]
       subj=esh[7]
       maxi=esh[8]
       negi=esh[9]


       if esh[10] !='':
        qi=esh[10]
       else:
        qi='-1'

       if esh[11] !='':
        oai=esh[11]
       else:
        oai='-1'
 
       if esh[12] !='':
        obi=esh[12]
       else:
        obi='-1'   

       if esh[13] !='':
        oci=esh[13]
       else:
        oci='-1'   

       if esh[14] !='':
        odi=esh[14]
       else:
        odi='-1'                 





  

       sql="insert into question(ques_statement,option_a,option_b,option_c,option_d,correct,sub,max_mark,nega_marks) values('"+ str(ques) +"','" + str(oa) +"','"+ str(ob)+ "','" + str(oc) + "','" + str(od) +"','" + str(corr) +"','"+ str(subj) + "','" +str(maxi) +"','" + str(negi) + "')"
       mycursor.execute(sql)
       mydb.commit() 
       
           
       sql= "select q_id from question where ques_statement ='"+ str(ques) + "' and  option_a ='" + str(oa) + "'"
       mycursor.execute(sql)
       result=mycursor.fetchall()
    
       test_id= session['exam_id']
       qu=result[0][0];
    
       sql="insert into rel_question_exam values (" + str(qu) + "," + str(test_id) + ")";
       mycursor.execute(sql)
       mydb.commit() 

       sql="insert into rel_image_question values (" + str(qu)  +","  +str(qi) +"," +str(oai) + "," + str(obi) + "," + str(oci) + "," + str(odi)+ ")";
       mycursor.execute(sql)
       mydb.commit() 

   
   
  return render_template('final_interface_t.html')



@app.route('/student_init/<id2>')
def index97(id2):
  session['check_it']='PASS_word'

  print("hello")
  sensor()
  return redirect("/student/" + str(id2))
  #return str("/student/" + str(id2))





@app.route('/student/<id2>')
def index15(id2):


  if(session.get('check_it')==None):
    return render_template('error_404_1.html')

  print("hello")
  sql="select batch ,i_id from student where s_id ="+ str(id2)
  mycursor.execute(sql)
  result=mycursor.fetchone()

  session['batch']=result[0]
  session['i_id']= result[1]
  session['student_id']= str(id2)


  sql=" select rel_institute_exam.e_id from rel_institute_exam join teacher on  teacher.t_id = rel_institute_exam.t_id where teacher.i_id=  "+ str(session['i_id']) + " and rel_institute_exam.batches like '%"  + str(session['batch']) + "%'"
  mycursor.execute(sql)
  results=mycursor.fetchall()


  ki='-1'
  for i in results:
      ki= ki+ "," + str(i[0]) 
 
      
  sql=" select e_id from exam where e_id in (" + str(ki) + ") and active=1 "
  mycursor.execute(sql)
  re=mycursor.fetchone()


  if re==None:
    return render_template('error_404_2.html')


  session['exam_id']=str(re[0])
  sql=" select q_id from rel_question_exam where e_id =" + str(re[0])
  mycursor.execute(sql)
  re=mycursor.fetchall()
  
  

  ki=''

  for i in re:
    ki= ki+  str(i[0]) 
    if i in re[:-1]:
      ki= ki + ","


  que= str(ki)

  sql= " select * from question where q_id in (" + que + ")";
  mycursor.execute(sql)
  results=mycursor.fetchall()



  sql=" select * from rel_image_question where q_id in (" + que + ")";
  mycursor.execute(sql)
  imgs=mycursor.fetchall()

  session['magic']= results




  sql=" select e_time,date from exam where e_id = " + str(session['exam_id']);
  mycursor.execute(sql)
  etime=mycursor.fetchone()

  # ki=etime[0].split(":")

  est=str(etime[0])
  dt = str(etime[1])
  et=est.split(":")
  ed=dt.split("-")

  le=len(results)



  re_write=list()

  for i in range(0,len(results)):
    local=list()

    for j in results[i]:
      local.append(j)

    for j in imgs[i]:
      local.append(j)

    re_write.append(local)


  
  return render_template('std_test.html',le=le,results=re_write,et=et,ed=ed,imgs=imgs,exid=str(session['exam_id']))

@app.route('/we.html')
def index16():
   final=request.values.get('final')
   
   correct_answer=session['magic']

   # return str(final)

   st= str(session['student_id'])
   st= st + ", " + str(final)


   st=st +  '\n';

   file = open(str(session['exam_id']) + '.csv','a')
   file.write(st) 
   file.close()

   session.clear()
   return render_template('final_interface_s.html')

   ca=list()
   for i in correct_answer:
    ca.append(i[6])

  # correct options are and responses are here

   return str(ca)















def sensor():
    """ Function for test purposes. """
    now = datetime.now()
    print("now =", now.time())
    c_date=now.date()
    c_time=now.time()

    sql="select e_id from exam where date= '"+ str(c_date) + "' and  s_time <= '" + str(c_time) + "' and  e_time >= '" +str(c_time) + "' and active='0' "
    print(sql)
    mycursor2.execute(sql)
    exam_identity=mycursor2.fetchall()


    print(exam_identity)

    for i in exam_identity:
      sql="update exam set active='1'  where e_id = " + str(i[0]) 
      mycursor2.execute(sql)
      mydb2.commit()
      mycursor.execute(sql)
      mydb.commit()
      print("test_started")




     
    sql="select e_id from exam where  active='1' and  date <= '"+ str(c_date) + "' and  e_time <= '" +str(c_time) + "'"
    print(str(sql))
    mycursor2.execute(sql)
    exam_identity=mycursor2.fetchall()


    sql="select e_id from exam where  active='1' and  date < '"+ str(c_date) + "'"
    print(str(sql))
    mycursor2.execute(sql)
    exam_identity2=mycursor2.fetchall()

    print(exam_identity)



    for i in exam_identity:
      sql="update exam set active='0'  where e_id =" + str(i[0]) 
      print(sql)
      mycursor2.execute(sql)
      mydb2.commit()

      mycursor.execute(sql)
      mydb.commit()


    for i in exam_identity2:
      sql="update exam set active='0'  where e_id =" + str(i[0]) 
      print(sql)
      mycursor2.execute(sql)
      mydb2.commit()

      mycursor.execute(sql)
      mydb.commit()


      print("test_completed")

        


# job_defaults = {
#     'coalesce': False,
#     'max_instances': 3
# }

# sched = BackgroundScheduler(job_defaults=job_defaults)
# sched.add_job(sensor,'interval',seconds=10)
# sched.start()




# @app.route("/home")
# def home():
#     """ Function for test purposes. """
#     return "Welcome Home :) !"




@app.route('/six/<test_id>')  
def upload(test_id):  
  #return ("hello")
    return render_template("file_upload_form.html",test_id=test_id)  
 
@app.route('/success/<test_id>', methods = ['POST'])  
def success(test_id):  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename) 


        sql="insert into img(image,test_id) values "



        val= str("'D:\\template") + str('@') +str(f.filename) +"'"
        val = val.replace("@", "\\")

        sql = sql + "(" + val + "," + str(test_id) + ")"

        mycursor.execute(sql)  
        mydb.commit()

        return render_template("success.html", name = f.filename)




@app.route('/ques_img.html')
def index25():
  return render_template('ques_img.html')


@app.route('/oa_img.html')
def index26():
  return render_template('oa_image.html')


@app.route('/ob_img.html')
def index27():
  return render_template('ob_image.html')


@app.route('/oc_img.html')
def index28():
  return render_template('oc_image.html')



@app.route('/od_img.html')
def index29():
  return render_template('od_image.html')


  
@app.route('/img_ques.html',methods=["POST"])
def index44():
  target=os.path.join(APP_ROOT,'static/ques_img/')
  print(target)

  if not os.path.isdir(target):
    os.mkdir(target)


  if(session.get('check_it')==None):
     return render_template('error_404_1.html')


  j=session['j']
  session['j']= session['j']+1
  for file in request.files.getlist("picq"):
      filename=str(session['exam_id'])  +"-" + file.name + str(j) + ".png"
      destination= "/".join([target,filename])
      print(destination)
      file.save(destination) 
      
      flash("Image Submitted")         

      return redirect('/ques_img.html')


@app.route('/img_oa.html',methods=["POST","GET"])
def index45():
  target=os.path.join(APP_ROOT,'static/ques_img/')
  print(target)

  if not os.path.isdir(target):
    os.mkdir(target)


  if(session.get('check_it')==None):
     return render_template('error_404_1.html')


  j=session['j']
  session['j']= session['j']+1
  for file in request.files.getlist("picq"):
      filename=str(session['exam_id'])  +"-" + file.name + str(j) + ".png"
      destination= "/".join([target,filename])
      print(destination)
      file.save(destination) 

      flash("Image Submitted")   

      return redirect('/oa_img.html')  


@app.route('/img_ob.html',methods=["POST"])
def index46():
  target=os.path.join(APP_ROOT,'static/ques_img/')
  print(target)

  if not os.path.isdir(target):
    os.mkdir(target)


  if(session.get('check_it')==None):
     return render_template('error_404_1.html')


  j=session['j']
  session['j']= session['j']+1
  for file in request.files.getlist("picq"):
      filename=str(session['exam_id'])  +"-" + file.name + str(j) + ".png"
      destination= "/".join([target,filename])
      print(destination)
      file.save(destination)    

      flash("Image Submitted")

      return redirect('/ob_img.html')            




@app.route('/img_oc.html',methods=["POST"])
def index47():
  target=os.path.join(APP_ROOT,'static/ques_img/')
  print(target)

  if not os.path.isdir(target):
    os.mkdir(target)


  if(session.get('check_it')==None):
     return render_template('error_404_1.html')


  j=session['j']
  session['j']= session['j']+1
  for file in request.files.getlist("picq"):
      filename=str(session['exam_id'])  +"-" + file.name + str(j) + ".png"
      destination= "/".join([target,filename])
      print(destination)
      file.save(destination)    

      flash("Image Submitted")

      return redirect('/oc_img.html')      



@app.route('/img_od.html',methods=["POST"])
def index48():
  target=os.path.join(APP_ROOT,'static/ques_img/')
  print(target)

  if not os.path.isdir(target):
    os.mkdir(target)


  if(session.get('check_it')==None):
     return render_template('error_404_1.html')


  j=session['j']
  session['j']= session['j']+1
  for file in request.files.getlist("picq"):
      filename=str(session['exam_id'])  +"-" + file.name + str(j) + ".png"
      destination= "/".join([target,filename])
      print(destination)
      file.save(destination)   

      flash("Image Submitted") 

      return redirect('/od_img.html')         