from django.shortcuts import render
from Blockchain import *
from Block import *
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
import io
import pandas as pd
import face_recognition
import os
from django.core.files.storage import default_storage
from django.conf import settings
import Database
import base64
from PIL import Image
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pickle
from django.templatetags.static import static
# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'AdminApp/Login.html')

def LogAction(request):
    username=request.POST['username']
    password=request.POST['password']

    if username=='Admin' and password=='Admin':
        return render(request,'AdminApp/AdminHome.html')
    else:
        context={'msg':'Login Failed...!!!'}
        return render(request,'AdminApp/Login.html',context)

def ahome(request):
     return render(request,'AdminApp/AdminHome.html')

def AddPartyDetails(request):
    return render(request,'AdminApp/AddParty.html')


blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def AddPartyAction(request):
    name=request.POST['name']
    record = 'none'
    for i in range(len(blockchain.chain)):
        if i>0:
            b=blockchain.chain[i]
            data=b.transactions[0]
            data=base64.b64decode(data)
            decrypt=blockchain.decrypt(data)
            decrypt=decrypt.decode("utf-8")
            arr=decrypt.split("#")
            if arr[0] == "AddParty":
                if arr[1]==name:
                    record="exits"
                    break
    if record=='none':
        data="AddParty#"+name
        enc=blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc),'utf-8')
        blockchain.add_new_transaction(enc)
        hash=blockchain.mine()
        b=blockchain.chain[len(blockchain.chain)-1]
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        context= {'msg':'Party Successfully Added...!!.','ph':'Previous HashCode: '+str(b.previous_hash),'bno':'BlockNo: '+str(b.index),'ch':"Current HashCode: "+str(b.hash)}
        return render(request, 'AdminApp/AddParty.html', context)
    else:
        context= {'msg':'Party already Registered'}
        return render(request, 'AdminApp/AddParty.html', context)

def AddCandidateDetails(request):
    strdata="<select name='pname' class='form-control' required>" \
                    "<option></option>"
    for i in range(len(blockchain.chain)):
        if i>0:
            b=blockchain.chain[i]
            data=b.transactions[0]
            data=base64.b64decode(data)
            decrypt=blockchain.decrypt(data)
            decrypt=decrypt.decode("utf-8")
            arr=decrypt.split("#")
            if arr[0] == "AddParty":
                strdata+="<option>"+arr[1]+"</option>"
    strdata+="</select>"
    context={'select':strdata}
    return render(request,'AdminApp/AddCandidate.html',context)

def AddCandidateAction(request):
    if request.method=='POST':
        partyname=request.POST['pname']
        candidatename=request.POST['candidatename']
        constituency=request.POST['constituency']
        image=request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save('./Static/Party/'+candidatename+'.png', image)

        record = 'none'
    for i in range(len(blockchain.chain)):
        if i>0:
            b=blockchain.chain[i]
            data=b.transactions[0]
            data=base64.b64decode(data)
            decrypt=blockchain.decrypt(data)
            decrypt=decrypt.decode("utf-8")
            arr=decrypt.split("#")
            if arr[0] == "AddCandidate":
                if arr[1]==partyname and arr[2]==candidatename and arr[3]==constituency:
                    record="exits"
                    break
    if record=='none':
        data="AddCandidate#"+partyname+"#"+candidatename+"#"+constituency
        enc=blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc),'utf-8')
        blockchain.add_new_transaction(enc)
        hash=blockchain.mine()
        b=blockchain.chain[len(blockchain.chain)-1]
        blockchain.save_object(blockchain,'blockchain_contract.txt')

        strdata="<select name='pname' class='form-control input-md' required>" \
                    "<option></option>"
        for i in range(len(blockchain.chain)):
            if i>0:
                b=blockchain.chain[i]
                data=b.transactions[0]
                data=base64.b64decode(data)
                decrypt=blockchain.decrypt(data)
                decrypt=decrypt.decode("utf-8")
                arr=decrypt.split("#")
                if arr[0] == "AddParty":
                    strdata+="<option>"+arr[1]+"</option>"
        strdata+="</select>"

        context= {'select':strdata,'msg':'Party Candidate Successfully Added...!!.','ph':'Previous HashCode: '+str(b.previous_hash),'bno':'BlockNo: '+str(b.index),'ch':"Current HashCode: "+str(b.hash)}
        return render(request, 'AdminApp/AddCandidate.html', context)
    else:
        strdata="<select name='pname' class='form-control input-md' required>" \
                    "<option></option>"
        for i in range(len(blockchain.chain)):
            if i>0:
                b=blockchain.chain[i]
                data=b.transactions[0]
                data=base64.b64decode(data)
                decrypt=blockchain.decrypt(data)
                decrypt=decrypt.decode("utf-8")
                arr=decrypt.split("#")
                if arr[0] == "AddParty":
                    strdata+="<option>"+arr[1]+"</option>"
        strdata+="</select>"
        context= {'select':strdata,'msg':'Party Candidate Already Added For this Constituency ..!!.'}
        return render(request, 'AdminApp/AddCandidate.html', context)

def ViewPartyDetails(request):
    output="<table class='table'><tr><thead class='thead-dark'>" \
            "<th scope='col'>Party Name</th>" \
           "<th scope='col'>Candidate Name</th>" \
           "<th scope='col'>Constituency Name</th>" \
           "<th scope='col'>Party Image</th>" \
           "</thead></tr>"

    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            if arr[0] == 'AddCandidate':
                output+="<tr><tbody><td scope='row'>"+arr[1]+"</td>"
                output+="<td scope='row'>"+arr[2]+"</td>"
                output+="<td scope='row'>"+arr[3]+"</td>"
                image_url = static(f'Party/{arr[2]}.png')
                output += f"<td><img src='{image_url}' width='100' height='100' alt='Party Image'></td></tbody></tr>"
    output+="</table>"
    context= {'table':output}
    return render(request, 'AdminApp/ViewCandidate.html', context)

def ViewVotes(request):
    con=Database.connect()
    cur=con.cursor()
    cur.execute("select * from votes ")
    data= cur.fetchall()

    output="<table class='table'><tr><thead class='thead-dark'>" \
            "<th scope='col'>Voter</th>" \
            "<th scope='col'>Party Name</th>" \
           "<th scope='col'>Candidate Name</th>" \
           "<th scope='col'>Constituency Name</th>" \
           "<th scope='col'>Party Image</th>" \
           "</thead></tr>"

    for d in data:
        party=d[2]
        cand=d[3]
        const=d[4]

        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == 'AddCandidate':
                    if arr[1]==party and arr[2]==cand and arr[3]==const:
                        output+="<tr><tbody><td scope='row'>"+d[1]+"</td>"
                        output+="<td scope='row'>"+arr[1]+"</td>"
                        output+="<td scope='row'>"+arr[2]+"</td>"
                        output+="<td scope='row'>"+arr[3]+"</td>"
                        image_url = static(f'Party/{arr[2]}.png')
                        output += f"<td><img src='{image_url}' width='100' height='100' alt='Party Image'></td></tbody></tr>"
    output+="</table>"
    context= {'table':output}
    return render(request, 'AdminApp/ViewVotes.html', context)

def ViewVotesCount(request):
    connection = Database.connect()  # Replace with your database connection logic
    query = """
    SELECT constituency, candidate, party, SUM(votes) as total_votes
    FROM votes
    GROUP BY constituency, candidate
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Convert to a DataFrame for easier manipulation
    df = pd.DataFrame(rows, columns=["Constituency", "Candidate", "Party", "Total Votes"])

    # Combine candidate and party name for display
    df["Candidate (Party)"] = df["Candidate"] + " (" + df["Party"] + ")"

    # Plot the graph using Matplotlib
    plt.figure(figsize=(12, 6))
    for constituency, group in df.groupby("Constituency"):
        plt.bar(
            group["Candidate (Party)"],
            group["Total Votes"],
            label=constituency
        )

    plt.title("Votes Per Candidate in Each Constituency")
    plt.xlabel("Candidate (Party)")
    plt.ylabel("Total Votes")
    plt.legend(title="Constituency", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()

    # Save the graph to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the graph as a base64 string
    graph = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'AdminApp/graph.html', {'graph': graph})

##VOTER OPERATIONS
def ulogin(request):
    return render(request,'UserApp/Login.html')

def register(request):
    return render(request,'UserApp/Register.html')

def RegAction(request):
    uname=request.POST['uname']
    email=request.POST['email']
    password=request.POST['password']
    const=request.POST['const']
    fingerprint_image=request.FILES.get('finger')
    profile_pic=request.FILES.get('profile')

    # Convert fingerprint image to base64
    fingerprint_image_base64 = None
    if fingerprint_image:
        with fingerprint_image.open() as f:
            fingerprint_image_base64 = base64.b64encode(f.read()).decode('utf-8')


    # Save files
    profile_path = default_storage.save(f"profile_pics/{profile_pic.name}", profile_pic)

    record = 'none'
    for i in range(len(blockchain.chain)):
        if i>0:
            b=blockchain.chain[i]
            data=b.transactions[0]
            data=base64.b64decode(data)
            decrypt=blockchain.decrypt(data)
            decrypt=decrypt.decode("utf-8")
            arr=decrypt.split("#")
            if arr[0] == "AddVoter":
                if  arr[2]==email and arr[3]==const:
                    record="exits"
                    break
    if record=='none':
        data="AddVoter#"+uname+"#"+email+"#"+const+"#"+password+"#"+profile_path+"#"+fingerprint_image_base64
        enc=blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc),'utf-8')
        blockchain.add_new_transaction(enc)
        hash=blockchain.mine()
        b=blockchain.chain[len(blockchain.chain)-1]
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        con=Database.connect()
        cur=con.cursor()
        cur.execute("insert into voter values(null,'"+email+"','"+profile_path+"')")
        con.commit()

        context= {"msg": "Registration successful!",'ph':'Previous HashCode: '+str(b.previous_hash),'bno':'BlockNo: '+str(b.index),'ch':"Current HashCode: "+str(b.hash)}
        return render(request, 'UserApp/Register.html', context)
    else:
        return render(request, "UserApp/Register.html", {"msg": "Username and Email Already Exist!"})




def UserLogAction(request):
    uname=request.POST['username']
    password=request.POST['password']
    const=request.POST['const']
    fingerprint_image=request.FILES.get('fingerprint')

    fingerprint_image_base64 = None
    with fingerprint_image.open() as f:
        fingerprint_image_base64 = base64.b64encode(f.read()).decode('utf-8')

    status = 'none'
    email = 'none'
    constituency = 'none'
    username= 'none'
    for i in range(len(blockchain.chain)):
        if i>0:
            b=blockchain.chain[i]
            data=b.transactions[0]
            data=base64.b64decode(data)
            decrypt=blockchain.decrypt(data)
            decrypt=decrypt.decode("utf-8")
            arr=decrypt.split("#")
            if arr[0] == "AddVoter":
                if arr[1]==uname and arr[3]==const and arr[4]==password and arr[6]==fingerprint_image_base64:
                    username = arr[1]
                    email = arr[2]
                    constituency = arr[3]
                    status = 'success'
                    break

    if status =='success':
        request.session['username']=username
        request.session['email']=email
        request.session['cost']=constituency
        return render(request, 'UserApp/VoterHome.html')
    else:
        context= {'data':'Login Failed Please Check Log Details'}
        return render(request, 'UserApp/Login.html', context)

def vhome(request):
    return render(request,'UserApp/VoterHome.html')

def CastVote(request):
    return render(request,'UserApp/CastVote.html')

@csrf_exempt
def CastVoteAction(request):
    if request.method == "POST":
        # Get image data for face and fingerprint
        image_data = request.POST['image']

        # Process face image (base64) into an actual image file
        image_data = image_data.split(",")[1]  # Remove the prefix part of base64
        image_binary = base64.b64decode(image_data)
        face_image = Image.open(BytesIO(image_binary))

        # Save the captured face image temporarily
        face_image_path = os.path.join(settings.MEDIA_ROOT, 'temp', 'captured_face.jpg')
        face_image.save(face_image_path)

        # Load the captured face and extract face encodings
        face_image = face_recognition.load_image_file(face_image_path)
        face_encodings = face_recognition.face_encodings(face_image)

        if not face_encodings:
            return JsonResponse({"success": False, "message": "No face detected"})

        captured_face_encoding = face_encodings[0]

        email=request.session['email']

        # Compare captured face with stored face encodings in the database
        query = "SELECT profile_pic from voter where email='"+email+"'"
        con=Database.connect()
        cursor=con.cursor()
        cursor.execute(query)
        users = cursor.fetchall()

        for user in users:
            profile_pic = user[0]  # profile_pic (extract it from the tuple)
            stored_image_path = os.path.join(settings.MEDIA_ROOT, profile_pic)


            # Load and compare the stored face encoding
            stored_face_image = face_recognition.load_image_file(stored_image_path)
            stored_face_encoding = face_recognition.face_encodings(stored_face_image)[0]

            if face_recognition.compare_faces([stored_face_encoding], captured_face_encoding)[0]:
                # If both face and fingerprint match, return successful response
                return JsonResponse({"success": True, "message": f"Welcome back, kishan!"})

        return JsonResponse({"success": False, "message": "Face not recognized"})

    return render(request, "UserApp/CastVote.html")

def ViewCandidateList(request):
    consti=request.session['cost']
    print(consti)
    output="<table class='table'><tr><thead class='thead-dark'>" \
            "<th scope='col'>Party Name</th>" \
           "<th scope='col'>Candidate Name</th>" \
           "<th scope='col'>Constituency Name</th>" \
           "<th scope='col'>Party Image</th>" \
           "<th scope='col'>Cast Vote</th>" \
           "</thead></tr>"

    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")

            if arr[0] == 'AddCandidate':
                a_con=str(arr[3]).lower()
                b_con=consti.lower()
                print(a_con)
                print(b_con)
                if a_con == b_con:
                    output+="<tr><tbody><td scope='row'>"+arr[1]+"</td>"
                    output+="<td scope='row'>"+arr[2]+"</td>"
                    output+="<td scope='row'>"+arr[3]+"</td>"
                    image_url = static(f'Party/{arr[2]}.png')
                    output += f"<td><img src='{image_url}' width='100' height='100' alt='Party Image'></td>"
                    output+="<td><a href='/RegsterVoter?pname="+str(arr[1])+"&candidatename="+str(arr[2])+"&cname="+str(arr[3])+"'\">Click</a></td></tbody></tr>"
    output+="</table>"
    context= {'table':output}
    return render(request, 'UserApp/ViewCandidates.html', context)

def RegsterVoter(request):
    email=request.session['email']
    pname=request.GET['pname']
    candidatename=request.GET['candidatename']
    cname=request.GET['cname']

    con=Database.connect()

    curr=con.cursor()
    curr.execute("select count(*) from votes where party='"+pname+"'and candidate='"+candidatename+"'and constituency='"+cname+"'")
    data=curr.fetchone()
    cc=0
    if data is not None:
        cc=data[0]
    if cc!=0:
        currr=con.cursor()
        currr.execute("select * from votes where voter_id='"+email+"' and party='"+pname+"'and candidate='"+candidatename+"'and constituency='"+cname+"'")
        data=currr.fetchone()
        if data is not None:
            return render(request, 'UserApp/VoteStatus.html', {'msg':'You have already used your vote!'})
        else:
            cur2=con.cursor()
            cur2.execute("insert into votes values(null,'"+email+"','"+pname+"','"+candidatename+"','"+cname+"','1')")
            con.commit()
            return render(request, 'UserApp/VoteStatus.html', {'msg':'Successfully Registered Your Vote!'})
    else:
        cur3=con.cursor()
        cur3.execute("insert into votes values(null,'"+email+"','"+pname+"','"+candidatename+"','"+cname+"','1')")
        con.commit()
        return render(request, 'UserApp/VoteStatus.html', {'msg':'Successfully Registered Your Vote!'})

def ViewVote(request):
    email=request.session['email']
    con=Database.connect()
    cur=con.cursor()
    cur.execute("select * from votes where voter_id='"+email+"'")
    data= cur.fetchall()

    output="<table class='table'><tr><thead class='thead-dark'>" \
            "<th scope='col'>Party Name</th>" \
           "<th scope='col'>Candidate Name</th>" \
           "<th scope='col'>Constituency Name</th>" \
           "<th scope='col'>Party Image</th>" \
           "</thead></tr>"

    for d in data:
        party=d[2]
        cand=d[3]
        const=d[4]

        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                data = base64.b64decode(data)
                decrypt = blockchain.decrypt(data)
                decrypt = decrypt.decode("utf-8")
                arr = decrypt.split("#")
                if arr[0] == 'AddCandidate':
                    if arr[1]==party and arr[2]==cand and arr[3]==const:
                        output+="<tr><tbody><td scope='row'>"+arr[1]+"</td>"
                        output+="<td scope='row'>"+arr[2]+"</td>"
                        output+="<td scope='row'>"+arr[3]+"</td>"
                        image_url = static(f'Party/{arr[2]}.png')
                        output += f"<td><img src='{image_url}' width='100' height='100' alt='Party Image'></td></tbody></tr>"
        output+="</table>"
    context= {'table':output}
    return render(request, 'UserApp/ViewVotes.html', context)


