import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {SettingComponent} from "./settings/settings.component";


const routes: Routes = [
  {path : "setting",component:SettingComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
