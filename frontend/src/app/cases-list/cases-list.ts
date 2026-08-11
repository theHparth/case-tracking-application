import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Cases, Case } from '../cases';

@Component({
  selector: 'app-cases-list',
  imports: [CommonModule],
  templateUrl: './cases-list.html',
  styleUrl: './cases-list.css',
})
export class CasesList implements OnInit {
  cases: Case[] = [];
  error = '';

  constructor(private casesService: Cases) {}

  ngOnInit(): void {
    this.casesService.list().subscribe({
      next: (data) => (this.cases = data),
      error: (err) => (this.error = 'Failed to load cases: ' + err.message),
    });
  }
}