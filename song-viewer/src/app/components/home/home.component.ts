import {Component, Input, OnInit, ViewChild} from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { SongProfile } from '../../models/song-profile'
import {Song} from "../../models/song";
import {HomeService} from "./home.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.sass'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ]
})
export class HomeComponent implements OnInit {
  displayedColumns: string[] = ['artist', 'song_name', 'emotion', 'size'];
  dataSource: MatTableDataSource<SongProfile>;
  expandedElement: SongProfile | null;
  nextPage: number;
  pageSize: number;
  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;
  @ViewChild(MatSort, { static: true }) sort: MatSort;

  db:SongProfile[] = new Array<SongProfile>();

  constructor(private homeService :HomeService) {

  }

  dataSubscription(letter:string, erase:boolean)
  {
    this.homeService.getAllRecordsByLetter(this.nextPage,this.pageSize, letter).then((records:SongProfile[]) => {
      this.nextPage +=1
      if(erase)
      {
        this.db = records;
      }
      else
      {
        this.db = [...this.db, ...records];
      }
      
      this.dataSource = new MatTableDataSource(this.db);

      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      if(records.length != 0)
      {
        this.dataSubscription(letter, false);
      }
    });
  }
  ngOnInit() {
    this.nextPage = 0
    this.pageSize = 1000
    this.dataSubscription('A', true);
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value.trim().toLowerCase();

    const filter = this.db.filter((profile : SongProfile) => {
          return profile.song.name.toLowerCase().includes(filterValue) ||
            profile.song.artist.toLowerCase().includes(filterValue) ||
            profile.emotion.includes(filterValue) ||
            profile.number_of_words.toString().includes(filterValue);
    });
    this.dataSource = new MatTableDataSource(filter);

    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  createHistogramChart(element:SongProfile)
  {
    let barChartData: any = [{data: Object.values(element.histogram), label: 'words'},];
    let barChartLabels:any = Object.keys(element.histogram);

    let barChartOptions: any = {
      scaleShowVerticalLines: true,
      responsive: true,
      maintainAspectRatio: true
    };

    let barChartLegend: any=true;
    let barChartType: any = 'bar';

    element.histogram.barChartData = barChartData;
    element.histogram.barChartLabels = barChartLabels;
    element.histogram.barChartOptions = barChartOptions;
    element.histogram.barChartLegend = barChartLegend;
    element.histogram.barChartType = barChartType;
    return element;
  }
  clickOnRow(element: any) {
    this.expandedElement = this.expandedElement === element ? null : element;
    if(this.expandedElement != null)
    {
     this.expandedElement = this.createHistogramChart(this.expandedElement);
    }
    
    
  }

  deleteDatabase()
  {
    this.homeService.deleteAllRecords();
    console.log("press delete")
  }
}
