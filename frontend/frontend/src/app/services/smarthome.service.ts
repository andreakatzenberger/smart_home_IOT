import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SmarthomeService {
  url = 'http://127.0.0.1:5000/';
  constructor(private http: HttpClient) { }

  get_last_measurement(measurement:string, device:string): Observable<any>{
    return this.http.get<any>(this.url + 'measurement/' + measurement + '/' + device);
  }

  stop_clock(): Observable<any>{
    return this.http.post<any>(this.url + 'stop_alarm', {});
  }
  activate_system(pin:string): Observable<any>{
    return this.http.put<any>(this.url + 'set_system_pin/' + pin, {});
  }
  deactivate_system(pin:string): Observable<any>{
    return this.http.put<any>(this.url + 'deactivate-safety-system/' + pin, {});
  }
  deactivate_system_alarm(): Observable<any>{
    return this.http.put<any>(this.url + 'deactivate-system_alarm', {});
  }
  get_alarm_on(): Observable<any>{
    return this.http.get<any>(this.url + 'get_alarm_status');

  }
  change_rgb_color(button_pressed:string): Observable<any>{
    return this.http.put<any>(this.url + 'rgb/' + button_pressed, {});
  }
}
