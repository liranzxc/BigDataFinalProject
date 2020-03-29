import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SettingComponent } from "./components/settings/settings.component";
import { HomeComponent } from './components/home/home.component';

const routes: Routes = [
  { path: "settings", component: SettingComponent },
  { path: "home/:id", component: HomeComponent },
  { path: "home", component: HomeComponent },
  { path: '**',   redirectTo: 'home/', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
