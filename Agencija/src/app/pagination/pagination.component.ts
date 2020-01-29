import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.scss']
})
export class PaginationComponent implements OnInit {

  @Input() max: number;
  @Input() current: number;
  @Output() get = new EventEmitter();

  constructor() { }

  ngOnInit() {
  }

  array() {
    return Array(this.max);
  }
}
