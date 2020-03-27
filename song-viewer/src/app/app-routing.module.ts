import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {TemplateBaseComponent} from "./template-base/template-base.component";


const routes: Routes = [
  {path : "statistic",component:TemplateBaseComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
