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

  ngOnInit() {
  }

}
