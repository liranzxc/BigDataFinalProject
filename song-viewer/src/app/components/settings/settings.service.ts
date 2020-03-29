import { Injectable } from '@angular/core';
import {SettingsForm} from "../../models/settings";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class SettingService {


  private URL_SERVER = "http://localhost:5000";

  constructor(private http:HttpClient) { }

  async CreateEnvFile(settingModel: SettingsForm) {
    const res:any = await this.http.post(this.URL_SERVER+"/createEnv",settingModel,
      {headers :{
          'Accept': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }}).toPromise();
   console.log(res);

  }

  async startProducer()
  {
    const res:any = await this.http.get(this.URL_SERVER+"/startProducer",
      {headers :{
          'Accept': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }}).toPromise();
    console.log(res);
    return res["state"];
  }

  async getConsumerState() {
    const res:any = await this.http.get(this.URL_SERVER+"/consumerState",
    {headers :{
        'Accept': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }}).toPromise();
 console.log(res);
 return res["state"];
  }

  async consumerDown() {
    const res:any = await this.http.get(this.URL_SERVER+"/stopConsumer",
    {headers :{
        'Accept': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }}).toPromise();
 console.log(res);
  }
}
