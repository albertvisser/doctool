function selectproj()
{
    document.getElementById('subThis').disabled=false;
    var h = document.getElementById("hProjNum");
    var i = document.getElementById('proj');
    h.value = i.value;
    alert(h.value + ", " + i.value)
}
function warnifproj0()
{
    document.MM_returnValue = true;
    var h = document.getElementById("hProjNum");
    if (h.value == "0")
    {
    alert("U moet wel eerst een project selecteren");
    document.MM_returnValue = false;
    }
}
