import {Component, OnInit, Input, ViewChild} from '@angular/core';
import {FormControl, FormGroup} from "@angular/forms";
import {SettingsForm} from "../../models/settings";
import {SettingService} from "./settings.service";
import {MatSlideToggle, MatSlideToggleChange} from "@angular/material/slide-toggle";

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.sass']
})
export class SettingComponent implements OnInit {


  private activate = new FormControl(false);

  private form:FormGroup;
  private settingModel : SettingsForm;

  private sentConfig:boolean = false;

  private numberOfWorkersOptions = [];
  private numberOfCoresOptions = [1,2];
  private memoryOptions = ["1g","2g","3g"];

  constructor(private settingService : SettingService) { }

  ngOnInit() {

    const numbers =  Array.from(Array(8).keys());
    numbers.shift();
    this.numberOfWorkersOptions =  numbers;

    this.settingModel = {
      memoryPerWorker:"1g",
      numOfWorkers:1,
      numOfCores:1
    } as SettingsForm;

    this.form = new FormGroup(
      {
        numOfWorkers : new FormControl(''),
        numOfCores : new FormControl(''),
        memoryPerWorker : new FormControl('')
      }
    );

     this.settingService.getConsumerState().then((state)=>{
       this.activate.patchValue(Boolean(state));
    });

  }

  submitConfigSetting() {

      this.settingModel = {...this.form.value} as SettingsForm;
      console.log(this.settingModel);

      this.settingService.CreateEnvFile(this.settingModel).then(
        () => {

          this.sentConfig = true;
        }
      );
  }

  toggleConsumer(ob :MatSlideToggleChange)
  {
    if(ob.checked) // true
    {
      if(this.form.valid)
      {
        this.submitConfigSetting();
      }
      else
      {
        this.activate.patchValue(false);
      }
    }
    else // false
    {
      this.settingService.consumerDown().then(console.log);
    }
  }

  startProducer() {
    this.settingService.startProducer().then(console.log);
  }
}
