import { Component } from '@angular/core';
import { UpdateWorkerService } from '../update-worker.service';
import { HlmCardDirective, HlmCardHeaderDirective, HlmCardTitleDirective, HlmCardDescriptionDirective, HlmCardContentDirective, HlmCardFooterDirective } from '@spartan-ng/ui-card-helm';


@Component({
  selector: 'app-statistics',
  standalone: true,
  imports: [HlmCardDirective, HlmCardHeaderDirective, HlmCardTitleDirective, HlmCardDescriptionDirective, HlmCardContentDirective, HlmCardFooterDirective],
  templateUrl: './statistics.component.html',
  styles: ``
})
export class StatisticsComponent {
  statistics: any = null;
  errorMessage: string = '';

  constructor(private updateWorkerService: UpdateWorkerService) {}

  ngOnInit(): void {
    this.updateWorkerService.data$.subscribe(
      data => {
        if (data) {
          this.statistics = this.calculateStatistics(data);
          this.errorMessage = ''
        } else {
          this.errorMessage = 'Error loading statistics data.';
        }
      },
      error => {
        this.errorMessage = 'Error loading statistics data.';
        console.error(error);
      }
    );
  }

  calculateStatistics(data: any): any {
    const total = data?.records.length;
    const free = data?.records.filter((p: { status: string; }) => p.status === 'Frei').length;
    const occupied = data?.records.filter((p: { status: string; }) => p.status === 'Besetzt').length;
    const reserved = data?.records.filter((p: { status: string | string[]; }) => p.status.includes('Reserviert')).length;
    const disabled = data?.records.filter((p: { status: string; }) => p.status === 'Deaktiviert').length;
    const special = data?.records.filter((p: { spezial: string; }) => p.spezial === '1').length;

    return { total, free, occupied, reserved, disabled ,special};
  }
}
