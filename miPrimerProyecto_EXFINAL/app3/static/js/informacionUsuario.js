
function cargarPub(idPub)
{
    fetch(`/obtenerDatosUsuario?idPub=${idPub}`)
    .then(response => response.json())
    .then(data => {
        tituloPub = document.getElementById('tituloPub')
        autorPub = document.getElementById('autorPub')
        descripcionPub = document.getElementById('descripcionPub')
        idPublicacion = document.getElementById('idPublicacion')
        comentariosTotales = document.getElementById('comentariosTotales')

        imagenPub = document.getElementById('imagenPub')

        if(data.imgPub !== null)
        {
            imagenPub.src = `data:image/jpeg;base64,${data.imgPub}`
            imagenPub.style.display = 'block'
        }
        else
        {
            imagenPub.style.display = 'none'
        }

        tituloPub.value = ''
        autorPub.value = ''
        descripcionPub.value = ''
        idPublicacion.innerHTML = ''
        comentariosTotales.innerHTML = ''

        tituloPub.value = data.titulo
        autorPub.value = data.autor
        descripcionPub.value = data.descripcion
        idPublicacion.innerHTML = String(idPub)

        for(let j = 0; j < data.datosComentarios.length; j++)
        {
            seccionComentario = `
            <div class="row mb-3">
                <div class="col-3">
                    ${data.datosComentarios[j].autor}
                </div>
                <div class="col-9">
                    ${data.datosComentarios[j].descripcion}
                </div>
            </div>
            `
            comentariosTotales.innerHTML = comentariosTotales.innerHTML + seccionComentario
        }
    })
}

function enviarComentario()
{
    comentarioUsuario = document.getElementById('comentarioUsuario')
    idPublicacion = document.getElementById('idPublicacion')

    datos = {
        'comentario':comentarioUsuario.value,
        'idPublicacion': idPublicacion.innerHTML
    }

    fetch('/publicarComentario',
    {
        method:"POST",
        headers:
        {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body:JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('comentarioUsuario').value = ''
        cargarPub(idPublicacion.innerHTML)
    })
}

function getCookie(name)
{
    let cookieValue = null;
    if (document.cookie && document.cookie !== "")
    {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++)
        {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "="))
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
/* cargarPub */ 
function cargarInformacionUsuario(idUsu)
{    
    console.log(idUsu)
    fetch(`/obtenerDatosUsuario?idUsuario=${idUsu}`)
    .then(response => response.json())
    .then(data => {
        idUsuario = document.getElementById('idUsuario')
        usernameUsuario = document.getElementById('usernameUsuario_1')
        nombreUsuario = document.getElementById('nombreUsuario_1')
        apellidoUsuario = document.getElementById('apellidoUsuario_1')
        profesionUsuario = document.getElementById('profesionUsuario_1')
        emailUsuario = document.getElementById('emailUsuario_1')
        nroCelular = document.getElementById('nroCelular_1')
        perfilUsuario = document.getElementById('perfilUsuario_1')

        idUsuario.value = ''
        usernameUsuario.value = ''
        nombreUsuario.value = ''
        apellidoUsuario.value = ''
        profesionUsuario.value = ''
        emailUsuario.value = ''
        nroCelular.value = ''
        perfilUsuario.innerHTML = ''
        
        idUsuario.innerHTML = String(idUsu)
        idUsuario.value = String(idUsu)
        usernameUsuario.value = data.usernameUsuario
        nombreUsuario.value = data.nombreUsuario
        apellidoUsuario.value = data.apellidoUsuario
        profesionUsuario.value = data.profesionUsuario
        emailUsuario.value = data.emailUsuario
        nroCelular.value = data.nroCelular
        perfilUsuario.innerHTML = data.perfilUsuario
    })
}