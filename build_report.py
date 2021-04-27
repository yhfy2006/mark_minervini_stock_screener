import json

def buildReport(file_path):
    strTable = "<!DOCTYPE html><html>" \
                '<head>' \
                '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>' \
               '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">' \
                '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap-theme.min.css" integrity="sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ" crossorigin="anonymous">' \
                '<script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>' \
               '<script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>'\
               """
                               <script type="text/javascript">
                               $(document).ready(function() {
                                $('#sortTable').DataTable();
                                } );
                               </script>
                               """ \
               '</head><body>'\
               '<table class="table table-striped table-bordered" id="sortTable">' \
                '<thead>'\
               '<tr><th class="th-sm">Ticket</th>' \
               '<th class="th-sm">Avg_Eps</th>' \
               '<th class="th-sm">Eps_1</th>' \
               '<th class="th-sm">Eps_2</th>' \
               '<th class="th-sm">Eps_3</th>' \
                "</tr> </thead>"
    strTable += '<tbody>'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for ticket_entry in data:
            print(ticket_entry)
            strRW = "<tr>" \
                    "<td>" + ticket_entry['ticket'] + "</td>" \
                    "<td>" + "{:.2f}".format(ticket_entry['avg_eps_abs'])+ "</td>" \
                    "<td>" + "{:.2f}".format(ticket_entry['details'][0]['abs_esp']) + "</td>" \
                    "<td>" + "{:.2f}".format(ticket_entry['details'][1]['abs_esp']) + "</td>" \
                    "<td>" + "{:.2f}".format(ticket_entry['details'][2]['abs_esp']) + "</td>" \
                    "</tr>"
            strTable += strRW


    strTable = strTable + "</tbody></table></body></html>"

    hs = open("report.html", 'w')
    hs.write(strTable)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help="file_path", type=str)
    args = parser.parse_args()

    buildReport(args.file)