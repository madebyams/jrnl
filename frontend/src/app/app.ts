import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div style="min-height: 100vh; background: #D9C6AF; padding: 2rem; display: flex; flex-direction: column;">
      <!-- Main content area -->
      <div style="flex: 1; display: flex; flex-direction: column; gap: 1rem; max-width: 56rem; margin: 0 auto; width: 100%;">
        <!-- Title -->
        <h1 style="text-align: center; font-family: monospace; font-size: 1.5rem; font-weight: bold; color: #000000; letter-spacing: -0.05em;">jrnl.</h1>
        <!-- Content textarea -->
        <div style="flex: 1; border: 1px solid #b8a38a; border-radius: 0.5rem; padding: 1rem; background: #ecdec9; display: flex; flex-direction: column;">
          <textarea
            [(ngModel)]="content"
            placeholder="Write your thoughts here..."
            style="flex: 1; background: transparent; color: #000000; outline: none; resize: none; font-family: monospace; font-size: 1rem; line-height: 1.5rem; border: none; min-height: calc(100vh - 8rem);"
            (keydown)="onKeydown($event)"
          ></textarea>
        </div>
      </div>
    </div>
  `
})
export class App {
  content = signal('');

  onKeydown(event: KeyboardEvent): void {
    if ((event.ctrlKey || event.metaKey) && event.key === 'a') {
      event.stopPropagation();
      const textarea = event.target as HTMLTextAreaElement;
      textarea.select();
    }
  }
}
