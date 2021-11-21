import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GrilleComponent } from './grille.component';

describe('GrilleComponent', () => {
  let component: GrilleComponent;
  let fixture: ComponentFixture<GrilleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GrilleComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GrilleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
