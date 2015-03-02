function clicked(){
    var searchFieldContent = $('#proteinId').val();
    $.post(
        '/viewer',
        {searchKeyword:searchFieldContent},
        function(retrievedData){
            console.log(retrievedData.json_list);
    });
}