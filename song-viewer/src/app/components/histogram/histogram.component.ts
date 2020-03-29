import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-histogram',
  templateUrl: './histogram.component.html',
  styleUrls: ['./histogram.component.sass']
})
export class HistogramComponent implements OnInit {

  @Input()
  barChartData: any;

  @Input()
  barChartLabels: any;

  @Input()
  barChartOptions: any;

  @Input()
  barChartLegend: any;

  @Input()
  barChartType: any;

  constructor() { }

  ngOnInit() {
  }

}
