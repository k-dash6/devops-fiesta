async function take_values (){
    document.getElementById("output").value = [];
    var checkboxes = document.getElementsByClassName('checkbox');
    var checkboxesChecked = []; // можно в массиве их хранить, если нужно использовать
    for (var index = 0; index < checkboxes.length; index++) {
        if (checkboxes[index].checked) {
            checkboxesChecked.push(checkboxes[index].value); // положим в массив выбранный
         }
      }
//    return checkboxesChecked; // для использования в нужном месте
    const result = await eel.convert_value_py(checkboxesChecked)();
    //document.getElementById("res").innerHTML+=result;
    document.getElementById("output").innerHTML = result;
    }

async function random_cocktail (){
    document.getElementById("output").value = [];
    var uncheck=document.getElementsByTagName('input');
     for(var i=0;i<uncheck.length;i++)
     {
      if(uncheck[i].type=='checkbox')
      {
       uncheck[i].checked=false;
      }
     }
    const result = await eel.decorator_for_random_cocktail()();
    document.getElementById("output").innerHTML = result;
    }

document.getElementById("submit").onclick = take_values;
document.getElementById("random").onclick = random_cocktail;