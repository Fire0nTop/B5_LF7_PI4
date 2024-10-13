import { Component, OnInit, Input } from '@angular/core';
import { UpdateWorkerService } from '../update-worker.service';
import {
  HlmCardContentDirective,
  HlmCardDescriptionDirective,
  HlmCardDirective,
  HlmCardFooterDirective,
  HlmCardHeaderDirective,
  HlmCardTitleDirective,
} from '@spartan-ng/ui-card-helm';
import { BrnSelectImports } from '@spartan-ng/ui-select-brain';
import { HlmSelectImports } from '@spartan-ng/ui-select-helm';
import { HlmSwitchModule } from "../../../spartan/ui-switch-helm/src/index";
import { FormsModule } from '@angular/forms';
import { DatabaseService } from '../database.service';
import { HlmInputDirective } from '@spartan-ng/ui-input-helm';

@Component({
  selector: 'app-parkplatz',
  templateUrl: './parkplatz.component.html',
  standalone: true,
  imports: [
    HlmCardDirective,
    HlmCardHeaderDirective,
    HlmCardTitleDirective,
    HlmCardDescriptionDirective,
    HlmCardContentDirective,
    HlmCardFooterDirective,
    BrnSelectImports,
    HlmSelectImports,
    HlmSwitchModule,
    FormsModule,
    HlmInputDirective
  ],
})
export class ParkplatzComponent implements OnInit {
  @Input() parkplatzId!: number;
  parkplatzData: any = null;
  formattedData: any = null;
  specificParkplatzData: any = null;
  errorMessage: string = '';

  constructor(
    private updateWorkerService: UpdateWorkerService,
    private databaseService: DatabaseService
  ) {}

  ngOnInit(): void {
    this.updateWorkerService.data$.subscribe(data => {
      this.parkplatzData = data;
      this.filterParkplatzData(data);
    });
  }

  filterParkplatzData(data: any): void {
    const found = data?.records.find((parkplatz: { key_id: number }) => parkplatz.key_id === this.parkplatzId);
    if (found) {
      this.specificParkplatzData = found;
      this.formattedData = this.specificParkplatzData;
      this.formattedData.spezial = Boolean(Number(this.formattedData.spezial));
      console.log(this.specificParkplatzData);
      this.errorMessage = '';
    } else {
      this.errorMessage = 'No data found for this Parkplatz ID.';
    }
  }

  onStatusChange(newStatus: string) {
    if (!this.specificParkplatzData) return;
    this.specificParkplatzData.status = newStatus;
    this.updateParkplatz();
  }

  onSpezialToggle(newSpezialValue: boolean) {
    if (!this.specificParkplatzData) return;
    this.specificParkplatzData.spezial = newSpezialValue;
    this.updateParkplatz();
  }

  // New methods to handle the Reihe and Nummer changes
  onReiheChange(newReihe: number) {
    if (!this.specificParkplatzData) return;
    this.specificParkplatzData.reihe = newReihe;
    this.updateParkplatz();
  }

  onNummerChange(newNummer: number) {
    if (!this.specificParkplatzData) return;
    this.specificParkplatzData.parkplatz_nummer = newNummer;
    this.updateParkplatz();
  }

  updateParkplatz() {
    const { key_id, reihe, parkplatz_nummer, arduino_id, arduino_parkplatz_id, status, spezial } = this.specificParkplatzData;

    this.databaseService.updateParkplatz(key_id, reihe, parkplatz_nummer, arduino_id, arduino_parkplatz_id, status, spezial)
      .subscribe({
        next: (response) => {
          if (response.status === 'success') {
            console.log('Update successful:', response);
          } else {
            this.errorMessage = 'Error updating the parkplatz data.';
          }
        },
        error: (error) => {
          this.errorMessage = 'Error updating the parkplatz data.';
          console.error('Error updating:', error);
        }
      });
  }

  getTimeAgo() {
    if (!this.specificParkplatzData) return '';

    const currentTime = Math.floor(Date.now() / 1000);
    const difference = currentTime - this.specificParkplatzData.zeitstempel;

    if (difference < 60) return `Vor ${difference} Sekunden`;
    else if (difference < 3600) return `Vor ${Math.floor(difference / 60)} Minuten`;
    else if (difference < 86400) return `Vor ${Math.floor(difference / 3600)} Stunden`;
    else return `Vor ${Math.floor(difference / 86400)} Tagen`;
  }
}

