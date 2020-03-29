import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {SongProfile} from "../../models/song-profile";

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  constructor(private http:HttpClient) { }
  private URL_SERVER = "http://localhost:5000";

  async getCounterMongodb()
  {
    const res:any = await this.http.get(this.URL_SERVER+"/mongodb/count",
      {headers :{
          'Accept': 'application/json'
        }}).toPromise();

    return res["total"];
  }

  async getAllRecords(page:number=0,size:number=5)
  {
    let res:SongProfile[] = await this.http.get<SongProfile[]>(`${this.URL_SERVER}/mongodb?page=${page}&size=${size}`,
      {headers :{
          'Accept': 'application/json'
        }}).toPromise();

      res = res.map(profile => {

        // @ts-ignore
        profile.song = JSON.parse(profile.song);
        return profile;

      });
    return res;
  }

  async deleteAllRecords()
  {
    const res:any = await this.http.delete(this.URL_SERVER+"/mongodb",
      {headers :{
          'Accept': 'application/json'
        }}).toPromise();

    console.log(res);
    return res["status"];
  }
}
