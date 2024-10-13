export interface Parkplatz {
  key_id: number;
  reihe: number;
  parkplatz_nummer: number;
  arduino_id: number;
  arduino_parkplatz_id: number;
  status: string;
  spezial: boolean;
  zeitstempel: number;
}

export interface ParkplatzResponse {
  status: string;
  records: Parkplatz[];
}
