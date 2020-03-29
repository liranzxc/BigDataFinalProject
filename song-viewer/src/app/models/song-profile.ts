import { Song } from './song'
export interface SongProfile {
  song : Song
  number_of_words :number;
  histogram : {
    barChartType?: any;
    barChartLegend?: any;
    barChartOptions?: any;
    barChartLabels?: any;
    barChartData?: any;
  };
  emotion :string;
}
