import { UpdateWorkerService } from './../update-worker.service';
import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HlmCardDirective, HlmCardHeaderDirective, HlmCardTitleDirective, HlmCardDescriptionDirective, HlmCardContentDirective, HlmCardFooterDirective } from '@spartan-ng/ui-card-helm';
import { BrnSelectImports } from '@spartan-ng/ui-select-brain';
import { HlmSelectImports } from '@spartan-ng/ui-select-helm';
import { HlmSwitchModule } from '@spartan-ng/ui-switch-helm';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
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
    FormsModule
  ],
  standalone:true,
})
export class HeaderComponent {
  @Output() statusChange = new EventEmitter<string>(); // Emit status changes
  selectedStatus: string = '';

  constructor() {}

  onStatusChange(newStatus: string) {
    this.selectedStatus = newStatus;
    this.statusChange.emit(newStatus); // Emit the new status
  }
}
