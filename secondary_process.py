import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar
import csv
import json
import argparse

class EPS:
    def __init__(self, processed_earning_abs_value, avg_eps_abs, ticket):
        self.processed_earning_abs_value = processed_earning_abs_value
        self.ticket = ticket
        self.avg_eps_abs = avg_eps_abs

    def getLastNEPSReport(self, n = 3):
        n_list = self.processed_earning_abs_value[:n]
        if len(n_list) > 0:
            self.avg_eps_abs = sum([x['abs_esp'] for x in n_list])/len(n_list)
            return {'ticket': self.ticket, 'avg_eps_abs': self.avg_eps_abs, 'details': n_list}
        else:
            return {'ticket': self.ticket, 'avg_eps_abs': 0, 'details': []}

class SecondaryProcess:
    datetimeNow = datetime.datetime.now()
    datetimeFrom = datetime.datetime.now() - datetime.timedelta(days=2 * 365)
    yec = YahooEarningsCalendar()
    target_eps = 0

    def object_decoder(self, obj):
        if '__type__' in obj and obj['__type__'] == 'EPS':
            return EPS(obj['details'], obj['avg_eps_abs'], obj['ticket'])
        return obj

    def processCSV(self, file_name, use_cache_file = True, *filters):
        if use_cache_file is not True:
            tickets = []
            with open(file_name) as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        ticket = row[1]
                        tickets.append(ticket)
                        line_count += 1
            results = [self.get_eps(x).getLastNEPSReport() for x in tickets]
        else:
            with open('secondary_process.json', ) as f:
                results = json.load(f, object_hook=self.object_decoder)

        for filter in filters:
            results = filter(results)


        with open('SecondaryResult.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)


    def filter_avg_eps(self, results):
        print('filter_avg_eps: before filtering, {}'.format(len(results)))
        filtered = [x for x in results if x['avg_eps_abs'] > self.target_eps]
        print('filter_avg_eps: after filtering, {}'.format(len(filtered)))
        return filtered


    def get_eps(self, ticket):
        try:
            earnings = self.yec.get_earnings_of(ticket)
        except:
            processed_earning_abs_value = [
                {'abs_esp': 0, 'eps_surprisepect':0,
                 'date': '2021-01-28T00:00:00.000Z'} ]
            return EPS(processed_earning_abs_value, 0, ticket)
        processed_earning_abs_value = [{'abs_esp': s['epsactual'] - s['epsestimate'], 'eps_surprisepect': s['epssurprisepct'], 'date': s['startdatetime']} for s in earnings if s['epsestimate'] is not None and s['epsactual'] is not None]
        eps = EPS(processed_earning_abs_value, 0, ticket)
        print('processing: {}'.format(ticket))
        return eps



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help="file_path", type=str)
    parser.add_argument('--eps', '-e', help="average_eps", type=float, default=0.25)
    args = parser.parse_args()

    processor = SecondaryProcess()
    processor.target_eps = args.eps
    processor.processCSV(args.file, False, processor.filter_avg_eps)
