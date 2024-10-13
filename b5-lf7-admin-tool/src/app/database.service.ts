import { environment } from './environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Method to execute SQL queries
  executeQuery(query: string): Observable<any> {
    const body = new URLSearchParams();
    body.set('query', query);

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    return this.http.post<any>(this.apiUrl, body.toString(), { headers });
  }

  // Additional methods can be defined here for specific queries
  getAllParkplätze(): Observable<any> {
    return this.executeQuery('SELECT * FROM parkplatz;');
  }

  findParkplatzById(id: number): Observable<any> {
    return this.executeQuery(`SELECT * FROM parkplatz WHERE key_id = ${id};`);
  }

  // Method to update a parking spot
  updateParkplatz(id: number, reihe: number, parkplatzNummer: number, arduinoId: number, arduinoParkplatzId: number, status: string, spezial: boolean): Observable<any> {
    const query = `
      UPDATE parkplatz
      SET reihe = ${reihe},
          parkplatz_nummer = ${parkplatzNummer},
          arduino_id = ${arduinoId},
          arduino_parkplatz_id = ${arduinoParkplatzId},
          status = '${status}',
          spezial = ${spezial ? 1 : 0},
          zeitstempel = UNIX_TIMESTAMP()
      WHERE key_id = ${id};
    `;
    return this.executeQuery(query);
  }

  // More methods can be added as needed...
}
