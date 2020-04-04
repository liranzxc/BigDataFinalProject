import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { SongProfile } from '../../models/song-profile'
import { HomeService } from "./home.service";
import { switchMap } from 'rxjs/operators';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { observable, Observable } from 'rxjs';
import * as uuid from 'uuid';

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
  lettersToShow: string[] = ['A', 'B', 'C', 'D', 'E', 'F', 'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];
  dataSource: MatTableDataSource<SongProfile>;
  expandedElement: SongProfile | null;
  nextPage: number = 0;
  pageSize: number = 100;
  currentJob: number = 0;
  totalRecords: number = 0;
  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;
  @ViewChild(MatSort, { static: true }) sort: MatSort;

  db: SongProfile[] = new Array<SongProfile>();

  constructor(private homeService: HomeService, private router: Router, private route: ActivatedRoute) {

  }

  ngOnInit() {
    this.homeService.getCounterMongodb().then(number =>
      this.totalRecords = number
    )
    this.updateData('', true, this.currentJob);
    this.route.paramMap.pipe(
      switchMap((params: ParamMap) =>
        params.getAll('id')
    )).subscribe((letter) => {
      console.log("fetching artists which begin with \"" + letter + "\"")
        if(letter == null)
        {
          letter = '';
        }
        
        const num: number = uuid.v4();
        this.currentJob = num;
        this.nextPage = 0;
        this.updateData(letter, true, num);
    })
    
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value.trim().toLowerCase();

    const filter = this.db.filter((profile: SongProfile) => {
      return profile.song_name.toLowerCase().includes(filterValue) ||
        profile.artist.toLowerCase().includes(filterValue) ||
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

  createHistogramChart(element: SongProfile) {
    let barChartData: any = [{ data: Object.values(element.histogram), label: 'words' },];
    let barChartLabels: any = Object.keys(element.histogram);

    let barChartOptions: any = {
      scaleShowVerticalLines: true,
      responsive: true,
      maintainAspectRatio: true
    };

    let barChartLegend: any = true;
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
    if (this.expandedElement != null) {
      this.expandedElement = this.createHistogramChart(this.expandedElement);
    }


  }

  updateData(letter: string, erase: boolean, job: number)
  {
    if(letter == '')
    {
      this.homeService.getAllRecords(this.nextPage, this.pageSize).then((records: SongProfile[]) => {
        if(this.currentJob == job)
        {
        this.nextPage += 1
        if(erase)
        {
          this.db = records
        }
        else
        {
          this.db = [...this.db, ...records];
        }
        this.dataSource = new MatTableDataSource(this.db);
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
        if (records.length != 0) {
          this.updateData(letter, false, job);
        }
      }
      });
    }
else
{


    this.homeService.getAllRecordsByLetter(this.nextPage, this.pageSize, letter).then((records: SongProfile[]) => {
      if(this.currentJob == job)
      {
      this.nextPage += 1
      if(erase)
      {
        this.db = records
      }
      else
      {
        this.db = [...this.db, ...records];
      }
      this.dataSource = new MatTableDataSource(this.db);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      if (records.length != 0) {
        this.updateData(letter, false, job);
      }
    }
    });
  }
  }
  deleteDatabase() {
    this.homeService.deleteAllRecords();
    console.log("press delete")
  }
}
