import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'app-template-base',
  templateUrl: './template-base.component.html',
  styleUrls: ['./template-base.component.sass']
})
export class TemplateBaseComponent implements OnInit {

  constructor(private router:Router) {
  }
  private statistic = 'statistic';
  private setting = 'setting';

  ngOnInit() {
  }

  openPage(url)
  {
    console.log(url);
   // this.router.navigate(url).then(console.log);
  }
}
