from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, FileResponse
from django.urls import reverse
from .models import publicacion, comentario, datosUsuario
import json
import base64
from django.contrib.auth.models import User


def ingresoUsuario(request):
    if request.method == 'POST':
        nombreUsuario = request.POST.get('nombreUsuario')
        contraUsuario = request.POST.get('contraUsuario')
        usrObj = authenticate(request,username=nombreUsuario, password=contraUsuario)
        if usrObj is not None:
            login(request,usrObj)
            return HttpResponseRedirect(reverse('app3:informacionUsuario'))
        else:
            return HttpResponseRedirect(reverse('app3:ingresoUsuario'))
    return render(request,'ingresoUsuario.html')

@login_required(login_url='/')
def informacionUsuario(request):
    return render(request,'informacionUsuario.html',{
        'allPubs':publicacion.objects.all()
    })


@login_required(login_url='/')
def cerrarSesion(request):
    logout(request)
    return render(request,'ingresoUsuario.html')

def ejemploJs(request):
    return render(request,'ejemploJs.html')

def devolverDatos(request):
    return JsonResponse(
        {
            'nombreCurso':'DesarroloWebPython',
            'horario':{
                'martes':'7-10',
                'jueves':'7-10'
            },
            'backend':'django',
            'frontend':'reactjs',
            'cantHoras':24
        }
    )

def devolverAllPubs(request):
    objPub = publicacion.objects.all()
    listaPublicacion = []
    for obj in objPub:
        listaPublicacion.append(
            {
                'titulo':obj.titulo,
                'descripcion':obj.descripcion
            }
        )
    return JsonResponse({
        'listaPublicacion':listaPublicacion
    })

def devolverPublicacion(request):
    idPub = request.GET.get('idPub')
    try:
        datosComentarios = []
        objPub = publicacion.objects.get(id=idPub)
        comentariosPub = objPub.comentario_set.all()
        for comentarioInfo in comentariosPub:
            datosComentarios.append({
                'autor': f"{comentarioInfo.autoCom.first_name} {comentarioInfo.autoCom.last_name}",
                'descripcion': comentarioInfo.descripcion
            })
        try:
            with open(objPub.imagenPub.path,'rb') as imgFile:
                imgPub = base64.b64encode(imgFile.read()).decode('UTF-8')
        except:
            imgPub = None

        return JsonResponse({
            'titulo': objPub.titulo,
            'autor':f"{objPub.autorPub.first_name} {objPub.autorPub.last_name}",
            'descripcion':objPub.descripcion,
            'datosComentarios': datosComentarios,
            'imgPub':imgPub
        })
    except:
        return JsonResponse({
            'titulo':'SIN DATOS',
            'autor':'SIN DATOS',
            'descripcion':'SIN DATOS',
            'datosComentarios':None,
            'imgPub':None
        })
    
def publicarComentario(request):
    datosComentario = json.load(request)
    comentarioTexto = datosComentario.get('comentario')
    idPublicacion = datosComentario.get('idPublicacion')
    objPublicacion = publicacion.objects.get(id=idPublicacion)
    comentario.objects.create(
        descripcion = comentarioTexto,
        pubRel = objPublicacion,
        autoCom = request.user
    )
    return JsonResponse({
        'resp':'ok'
    })

def crearPublicacion(request):
    if request.method == 'POST':
        tituloPub = request.POST.get('tituloPub')
        descripcionPub = request.POST.get('descripcionPub')
        autorPub = request.user
        imagenPub = request.FILES.get('imagenPub')

        publicacion.objects.create(
            titulo=tituloPub,
            descripcion=descripcionPub,
            autorPub = autorPub,
            imagenPub = imagenPub
        )

        return HttpResponseRedirect(reverse('app3:informacionUsuario'))
    
def inicioReact(request):
    return render(request, 'inicioReact.html')

#EXAMEN FINAL - Crea usuario
def crearUsuario(request):
    if request.method == 'POST':
        usernameUsuario = request.POST.get('usernameUsuario')
        contraUsuario = request.POST.get('contraUsuario')
        nombreUsuario = request.POST.get('nombreUsuario')
        apellidoUsuario = request.POST.get('apellidoUsuario')
        emailUsuario = request.POST.get('emailUsuario')
        profesionUsuario = request.POST.get('profesionUsuario')
        nroCelular = request.POST.get('nroCelular')
        perfilUsuario = request.POST.get('perfilUsuario')

        nuevoUsuario = User.objects.create(
            username=usernameUsuario,
            email=emailUsuario
        )
        nuevoUsuario.set_password(contraUsuario)
        nuevoUsuario.first_name = nombreUsuario
        nuevoUsuario.last_name = apellidoUsuario
        nuevoUsuario.is_staff = True
        nuevoUsuario.save()

        datosUsuario.objects.create(
            profesion=profesionUsuario,
            nroCelular=nroCelular,
            perfilUsuario=perfilUsuario,
            usrRel=nuevoUsuario
        )

        return HttpResponseRedirect(reverse('app3:consolaAdministrador'))

@login_required(login_url='/')
def consolaAdministrador(request):
    allUsers = User.objects.all().order_by('id')
    return render(request,'consolaAdministrador.html',{
        'allUsers':allUsers
    })

@login_required(login_url='/')
def obtenerDatosUsuario(request):
    idUsuario = request.GET.get('idUsuario')
    try:
        objUsu = User.objects.get(id=idUsuario)
        objUsuDatos = datosUsuario.objects.get(usrRel=idUsuario)
        return JsonResponse({
            'idUsuario': objUsu.id,
            'usernameUsuario': objUsu.username,
            'nombreUsuario': objUsu.first_name,
            'apellidoUsuario': objUsu.last_name,
            'profesionUsuario': objUsuDatos.profesion,
            'emailUsuario': objUsu.email,
            'nroCelular': objUsuDatos.nroCelular,
            'perfilUsuario': objUsuDatos.perfilUsuario
        })
    except:
        return JsonResponse({   
            'idUsuario': 'SIN DATOS',      
            'usernameUsuario': 'SIN DATOS',
            'nombreUsuario': 'SIN DATOS',
            'apellidoUsuario': 'SIN DATOS',
            'profesionUsuario': 'SIN DATOS',
            'emailUsuario': 'SIN DATOS',
            'nroCelular': 'SIN DATOS',
            'perfilUsuario': None
        })

@login_required(login_url='/')
def actualizarUsuario(request):    
    if request.method == 'POST':
        print("<<====================================================================>>")
        idUsuario = request.POST.get('idUsuario')
        ##usernameUsuario = request.POST.get('usernameUsuario')
        nombreUsuario = request.POST.get('nombreUsuario')
        apellidoUsuario = request.POST.get('apellidoUsuario')
        profesionUsuario = request.POST.get('profesionUsuario')
        ##emailUsuario = request.POST.get('emailUsuario')
        nroCelular = request.POST.get('nroCelular')
        perfilUsuario = request.POST.get('perfilUsuario')

        updateUsuario = User.objects.get(id=idUsuario)
        updateUsuario.first_name = nombreUsuario
        updateUsuario.last_name = apellidoUsuario
        updateUsuario.is_staff = True
        updateUsuario.save()

        updateUsuarioDatos = datosUsuario.objects.get(usrRel=idUsuario)
        updateUsuarioDatos.profesion = profesionUsuario
        updateUsuarioDatos.nroCelular = nroCelular
        updateUsuarioDatos.perfilUsuario = perfilUsuario
        updateUsuarioDatos.save()

        return HttpResponseRedirect(reverse('app3:consolaAdministrador'))

    return HttpResponseRedirect(reverse('app4:consolaAdministrador'))

