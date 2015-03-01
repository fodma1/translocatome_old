function clicked(){
    var searchFieldContent = $('#proteinId').val();
    $.post(
        '/viewer',
        {searchKeyword:searchFieldContent},
        function(retrievedData){
            alert(retrievedData);
    });
}