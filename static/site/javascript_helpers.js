$("#id_nhl_form-starting_country").change(function () {
    var url = $("#form").attr("data-cities-url");  // get the url of the load provinces page
    var country = $(this).val();  // get the selected country

    $.ajax({
        url: url,
        data: {
            'country': country
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
            // replace the contents of the city input with the data that came from the server
            $("#id_nhl_form-starting_province").html(data);
        }
    });

});

function sortTable(n) {
    // TODO replace bubble sort with a faster sorting algorithm
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("nhl-game-table");
    switching = true;
    // Set the sorting direction to ascending:
    dir = "asc";
    // Make a loop that will continue until no switching has been done
    while (switching) {
        // Start by saying no switching is done
        switching = false;
        rows = table.rows;
        // Loop through all table rows (except the first 2, which contains table headers and filter inputs)
        for (i = 2; i < (rows.length - 1); i++) {
            // Start by saying there should be no switching
            shouldSwitch = false;
            // Get the two elements you want to compare, one from current row and one from the next
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            // Check if the two rows should switch place, based on the direction, asc or desc
            if (dir == "asc") {
                if(n == 3) {
                    // Need to sort using numbers since its the distance column
                    if (parseInt(x.innerHTML.replace(',', '')) > parseInt(y.innerHTML.replace(',', ''))) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                }
                else {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                }
            } else if (dir == "desc") {
                if (n == 3) {
                    // Need to sort using numbers since its the distance column
                    if (parseInt(x.innerHTML.replace(',', '')) < parseInt(y.innerHTML.replace(',', ''))) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                }
                else {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                }
            }
        }
        if (shouldSwitch) {
            // If a switch has been marked, make the switch and mark that a switch has been done
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // Each time a switch is done, increase this count by 1:
            switchcount ++;
        } else {
            // If no switching has been done AND the direction is "asc", set the direction to "desc" and run the while loop again.
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}