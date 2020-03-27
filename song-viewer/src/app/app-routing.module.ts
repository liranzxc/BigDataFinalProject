import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {SettingComponent} from "./setting/setting.component";
import { HomeComponent } from './components/home/home.component';

const routes: Routes = [
  {path : "setting",component:SettingComponent},
  {path : "home",component:HomeComponent}
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
