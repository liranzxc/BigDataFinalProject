import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {SettingService} from "./settings.service";

@NgModule({
  declarations: [],
  exports : [],
  providers : [SettingService],
  imports: [
    CommonModule
  ]
})
export class SettingModule { }
