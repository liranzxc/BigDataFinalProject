import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import {animate, state, style, transition, trigger} from '@angular/animations';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.sass'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ]
})
export class HomeComponent implements OnInit {
  displayedColumns: string[] = ['artist', 'name', 'emotion', 'size'];
  dataSource: MatTableDataSource<SongProfile>;
  expandedElement: SongProfile | null;

  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;
  @ViewChild(MatSort, { static: true }) sort: MatSort;

  constructor() {
    // Create 100 users
    const songProfiles = Array.from({ length: 2000 }, (_, k) => createNewSongProfile(k + 1));

    // Assign the data to the data source for the table to render
    this.dataSource = new MatTableDataSource(songProfiles);

  }

  ngOnInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}
export interface SongProfile {
  artist: string;
  name: string;
  lyrics: string;

  size: number;
  emotion: string;
  histogram: object;
}

export interface Song {
  artist: string;
  name: string;
  lyrics: string;
}
/** Constants used to fill up our data base. */
const SONG_NAMES: string[] = [
  'maroon', 'red', 'orange', 'yellow', 'olive', 'green', 'purple', 'fuchsia', 'lime', 'teal',
  'aqua', 'blue', 'navy', 'black', 'gray'
];
const ARTISTS: string[] = [
  'Maia', 'Asher', 'Olivia', 'Atticus', 'Amelia', 'Jack', 'Charlotte', 'Theodore', 'Isla', 'Oliver',
  'Isabella', 'Jasper', 'Cora', 'Levi', 'Violet', 'Arthur', 'Mia', 'Thomas', 'Elizabeth'
];

const EMOTIONS: string[] = [
  'Happy', 'Sad', 'Angry', 'Hateful', 'Joyful'
];

/** Builds and returns a new User. */
function createNewSongProfile(id: number): SongProfile {

  const artist = ARTISTS[Math.round(Math.random() * (ARTISTS.length - 1))];

  const emotion = EMOTIONS[Math.round(Math.random() * (EMOTIONS.length - 1))];

  const song_name = SONG_NAMES[Math.round(Math.random() * (SONG_NAMES.length - 1))];

  return {
    artist: artist,
    name: song_name,
    lyrics: 'djhf sdfisad sdlfksd',
    size: Math.round(Math.random() * 1000),
    emotion: emotion,
    histogram: {
      'a': Math.random(),
      'b': Math.random(),
      'c': Math.random()
    }
  };

};

