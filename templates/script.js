alert(1);
fetch("http://127.0.0.1:5000/emplist").then((data)=>{
     return data.json();
}).then((objectData)=>{
    console.log(objectData[0].date_created);
    let tableData="";
    objectData.map((values)=>{
        tableData+=`<tr>
        <td>${values.id}</td>
        <td>${values.description}</td>
        <td>${values.name}</td>
        <td>${values.date_created}</td>
        <td><input type ="submit" name="Update" value="Update"/><input type ="submit" name="Delete" value="Delete"/></td>
      </tr>`;
    });
    document.getElementById("table_body").innerHTML=tableData;
})