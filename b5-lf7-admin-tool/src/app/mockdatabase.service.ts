import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { cloneDeep } from 'lodash'; // Import lodash or any deep cloning utility

@Injectable({
  providedIn: 'root'
})
export class MockDatabaseService {
  private mockData = [
    { key_id: 1, reihe: 1, parkplatz_nummer: 1, arduino_id: 101, arduino_parkplatz_id: 201, status: 'Frei', spezial: false, zeitstempel: 1728765226 },
    { key_id: 2, reihe: 1, parkplatz_nummer: 2, arduino_id: 101, arduino_parkplatz_id: 202, status: 'Besetzt', spezial: true, zeitstempel: 1728765226 },
    { key_id: 3, reihe: 1, parkplatz_nummer: 3, arduino_id: 101, arduino_parkplatz_id: 203, status: 'Reserviert (System)', spezial: true, zeitstempel: 1728765226 },
    // Add more mock data as needed
  ];

  // Method to retrieve all parkplätze
  getAllParkplätze(): Observable<any> {
    return of({ status: 'success', records: cloneDeep(this.mockData) });
  }

  // Method to find a specific parkplatz by ID
  findParkplatzById(id: number): Observable<any> {
    const record = this.mockData.find(item => item.key_id === id);
    return of({ status: 'success', records: record ? [cloneDeep(record)] : [] });
  }

  // Method to update parkplatz data
  updateParkplatz(id: number, reihe: number, parkplatzNummer: number, arduinoId: number, arduinoParkplatzId: number, status: string, spezial: boolean): Observable<any> {
    const index = this.mockData.findIndex(item => item.key_id === id);
    if (index === -1) {
      return of({ status: 'error', message: 'Parkplatz not found' });
    }

    // Update the record properties directly
    this.mockData[index].reihe = reihe;
    this.mockData[index].parkplatz_nummer = parkplatzNummer;
    this.mockData[index].arduino_id = arduinoId;
    this.mockData[index].arduino_parkplatz_id = arduinoParkplatzId;
    this.mockData[index].status = status;
    this.mockData[index].spezial = spezial;

    return of({ status: 'success', affected_rows: 1 });
  }
}
