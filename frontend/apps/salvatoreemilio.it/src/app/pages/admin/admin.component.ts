import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'frontend-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    console.log("AdminComponent ngOnInit()")
  }

}
