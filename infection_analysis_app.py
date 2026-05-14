#!/usr/bin/env python3
"""
Приложение для анализа распространения заражения.
Принимает файл с координатами точек заражения, находит очаги (источники)
и прогнозирует дальнейшее распространение.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import cdist
import json
import csv
import os


class InfectionSpreadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ распространения заражения")
        self.root.geometry("1200x800")
        
        # Данные
        self.points = None
        self.sources = None
        self.prediction_points = None
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Верхняя панель управления
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Кнопка загрузки файла
        self.load_btn = ttk.Button(control_frame, text="Загрузить файл с координатами", 
                                   command=self.load_file)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Параметры кластеризации
        ttk.Label(control_frame, text="Eps (радиус):").pack(side=tk.LEFT, padx=5)
        self.eps_var = tk.DoubleVar(value=50.0)
        self.eps_spin = ttk.Spinbox(control_frame, from_=1.0, to=500.0, 
                                    width=10, textvariable=self.eps_var)
        self.eps_spin.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Min Samples:").pack(side=tk.LEFT, padx=5)
        self.min_samples_var = tk.IntVar(value=5)
        self.min_samples_spin = ttk.Spinbox(control_frame, from_=2, to=100, 
                                            width=10, textvariable=self.min_samples_var)
        self.min_samples_spin.pack(side=tk.LEFT, padx=5)
        
        # Кнопка анализа
        self.analyze_btn = ttk.Button(control_frame, text="Найти очаги заражения", 
                                      command=self.analyze_data, state=tk.DISABLED)
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка прогноза
        self.predict_btn = ttk.Button(control_frame, text="Спрогнозировать распространение", 
                                      command=self.predict_spread, state=tk.DISABLED)
        self.predict_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка очистки
        self.clear_btn = ttk.Button(control_frame, text="Очистить", 
                                    command=self.clear_data)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Статус
        self.status_var = tk.StringVar(value="Ожидание загрузки файла...")
        self.status_label = ttk.Label(control_frame, textvariable=self.status_var, 
                                      foreground="blue")
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Основная область с графиками
        main_frame = ttk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Левая часть - исходные данные и очаги
        left_frame = ttk.LabelFrame(main_frame, text="Карта заражения", padding="5")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.fig1 = Figure(figsize=(6, 5), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=left_frame)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Правая часть - прогноз
        right_frame = ttk.LabelFrame(main_frame, text="Прогноз распространения", padding="5")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.fig2 = Figure(figsize=(6, 5), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=right_frame)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Панель информации
        info_frame = ttk.LabelFrame(self.root, text="Информация", padding="10")
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.info_text = tk.Text(info_frame, height=6, wrap=tk.WORD)
        self.info_text.pack(fill=tk.X, expand=True)
        
        # Scrollbar для текста
        scrollbar = ttk.Scrollbar(self.info_text, orient=tk.VERTICAL, command=self.info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
    def load_file(self):
        """Загрузка файла с координатами"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл с координатами",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("CSV файлы", "*.csv"),
                ("JSON файлы", "*.json"),
                ("Все файлы", "*.*")
            ]
        )
        
        if not file_path:
            return
            
        try:
            self.points = self.parse_file(file_path)
            
            if len(self.points) == 0:
                messagebox.showerror("Ошибка", "Не удалось найти координаты в файле")
                return
                
            self.status_var.set(f"Загружено {len(self.points)} точек")
            self.analyze_btn.config(state=tk.NORMAL)
            
            # Отображение загруженных точек
            self.plot_original_data()
            
            self.info_text.insert(tk.END, f"✓ Загружен файл: {os.path.basename(file_path)}\n")
            self.info_text.insert(tk.END, f"✓ Количество точек: {len(self.points)}\n")
            self.info_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
            
    def parse_file(self, file_path):
        """Парсинг файла с координатами"""
        points = []
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, (list, tuple)) and len(item) >= 2:
                            points.append([float(item[0]), float(item[1])])
                        elif isinstance(item, dict):
                            x = item.get('x') or item.get('lon') or item.get('longitude')
                            y = item.get('y') or item.get('lat') or item.get('latitude')
                            if x is not None and y is not None:
                                points.append([float(x), float(y)])
                                
        elif ext == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        try:
                            x, y = float(row[0]), float(row[1])
                            points.append([x, y])
                        except ValueError:
                            continue
                            
        else:  # TXT и другие форматы
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    # Разделители: пробел, запятая, таб
                    parts = line.replace(',', ' ').replace('\t', ' ').split()
                    if len(parts) >= 2:
                        try:
                            x, y = float(parts[0]), float(parts[1])
                            points.append([x, y])
                        except ValueError:
                            continue
                            
        return np.array(points) if points else np.array([])
        
    def plot_original_data(self):
        """Отображение исходных данных"""
        self.ax1.clear()
        
        if self.points is not None and len(self.points) > 0:
            self.ax1.scatter(self.points[:, 0], self.points[:, 1], 
                           c='blue', alpha=0.6, s=30, label='Точки заражения')
            self.ax1.set_xlabel('X координата')
            self.ax1.set_ylabel('Y координата')
            self.ax1.set_title('Карта зараженных точек')
            self.ax1.grid(True, alpha=0.3)
            self.ax1.legend()
            
        self.canvas1.draw()
        
    def analyze_data(self):
        """Анализ данных и поиск очагов заражения"""
        if self.points is None or len(self.points) == 0:
            messagebox.showwarning("Предупреждение", "Сначала загрузите данные")
            return
            
        eps = self.eps_var.get()
        min_samples = self.min_samples_var.get()
        
        try:
            # Используем DBSCAN для кластеризации
            db = DBSCAN(eps=eps, min_samples=min_samples).fit(self.points)
            labels = db.labels_
            
            # Находим центры кластеров (очаги заражения)
            unique_labels = set(labels)
            self.sources = []
            
            for label in unique_labels:
                if label == -1:  # Шум
                    continue
                cluster_points = self.points[labels == label]
                center = np.mean(cluster_points, axis=0)
                self.sources.append({
                    'center': center,
                    'points_count': len(cluster_points),
                    'radius': np.max(np.linalg.norm(cluster_points - center, axis=1))
                })
                
            # Отображение результатов
            self.plot_sources(labels)
            
            # Информация
            self.info_text.insert(tk.END, f"\n✓ Анализ завершен\n")
            self.info_text.insert(tk.END, f"✓ Найдено очагов: {len(self.sources)}\n")
            for i, source in enumerate(self.sources):
                self.info_text.insert(tk.END, 
                    f"  Очаг {i+1}: центр ({source['center'][0]:.2f}, {source['center'][1]:.2f}), "
                    f"точек: {source['points_count']}, радиус: {source['radius']:.2f}\n")
            self.info_text.see(tk.END)
            
            self.status_var.set(f"Найдено {len(self.sources)} очагов заражения")
            self.predict_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при анализе:\n{str(e)}")
            
    def plot_sources(self, labels):
        """Отображение очагов заражения"""
        self.ax1.clear()
        
        # Отображение всех точек цветом по кластерам
        unique_labels = set(labels)
        colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))
        
        for i, label in enumerate(unique_labels):
            if label == -1:  # Шум
                mask = labels == -1
                self.ax1.scatter(self.points[mask, 0], self.points[mask, 1], 
                               c='gray', alpha=0.3, s=20, label='Шум')
            else:
                mask = labels == label
                self.ax1.scatter(self.points[mask, 0], self.points[mask, 1], 
                               c=[colors[i]], alpha=0.6, s=30, 
                               label=f'Кластер {label}')
                               
        # Отображение центров очагов
        if self.sources:
            centers = np.array([s['center'] for s in self.sources])
            self.ax1.scatter(centers[:, 0], centers[:, 1], 
                           c='red', s=200, marker='X', 
                           label='Очаги заражения', edgecolors='black', linewidths=2)
                           
            # Радиусы очагов
            for source in self.sources:
                circle = plt.Circle(source['center'], source['radius'], 
                                  color='red', fill=False, linestyle='--', alpha=0.5)
                self.ax1.add_patch(circle)
                
        self.ax1.set_xlabel('X координата')
        self.ax1.set_ylabel('Y координата')
        self.ax1.set_title('Очаги заражения')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.legend(loc='best', fontsize=8)
        
        self.canvas1.draw()
        
    def predict_spread(self):
        """Прогнозирование распространения заражения"""
        if not self.sources:
            messagebox.showwarning("Предупреждение", "Сначала найдите очаги заражения")
            return
            
        try:
            self.ax2.clear()
            
            # Параметры распространения
            spread_speed = 30  # Скорость распространения (условных единиц)
            time_steps = [1, 3, 5]  # Прогноз на 1, 3, 5 временных шагов
            
            # Создаем сетку для визуализации
            x_min, x_max = self.points[:, 0].min() - 50, self.points[:, 0].max() + 50
            y_min, y_max = self.points[:, 1].min() - 50, self.points[:, 1].max() + 50
            xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                               np.linspace(y_min, y_max, 200))
            grid_points = np.c_[xx.ravel(), yy.ravel()]
            
            # Расчет зон заражения для разных временных шагов
            infection_levels = np.zeros(len(grid_points))
            
            for source in self.sources:
                center = source['center']
                initial_radius = source['radius']
                
                # Расстояние от каждой точки сетки до центра очага
                distances = np.linalg.norm(grid_points - center, axis=1)
                
                # Для каждого временного шага рассчитываем зону заражения
                for t in time_steps:
                    current_radius = initial_radius + spread_speed * t
                    infected_mask = distances <= current_radius
                    infection_levels[infected_mask] = np.maximum(
                        infection_levels[infected_mask], t)
                        
            # Визуализация прогноза
            contourf = self.ax2.contourf(xx, yy, infection_levels.reshape(xx.shape), 
                                        levels=[0, 1, 3, 5], 
                                        colors=['white', 'yellow', 'orange', 'red'],
                                        alpha=0.7)
            
            # Добавляем исходные точки
            self.ax2.scatter(self.points[:, 0], self.points[:, 1], 
                           c='blue', alpha=0.5, s=20, label='Исходные точки')
            
            # Центры очагов
            if self.sources:
                centers = np.array([s['center'] for s in self.sources])
                self.ax2.scatter(centers[:, 0], centers[:, 1], 
                               c='red', s=150, marker='X', 
                               label='Очаги', edgecolors='black')
                               
            # Границы зон заражения для каждого временного шага
            for t in time_steps:
                for source in self.sources:
                    radius = source['radius'] + spread_speed * t
                    circle = plt.Circle(source['center'], radius, 
                                      fill=False, linestyle='-', 
                                      linewidth=1.5, alpha=0.8,
                                      label=f'Прогноз t={t}' if source == self.sources[0] else "")
                    self.ax2.add_patch(circle)
                    
            self.ax2.set_xlabel('X координата')
            self.ax2.set_ylabel('Y координата')
            self.ax2.set_title('Прогноз распространения заражения')
            self.ax2.grid(True, alpha=0.3)
            self.ax2.legend(loc='best', fontsize=8)
            self.ax2.set_xlim(x_min, x_max)
            self.ax2.set_ylim(y_min, y_max)
            
            self.canvas2.draw()
            
            # Информация о прогнозе
            self.info_text.insert(tk.END, f"\n✓ Прогноз построен\n")
            self.info_text.insert(tk.END, f"✓ Скорость распространения: {spread_speed} ед./шаг\n")
            self.info_text.insert(tk.END, f"✓ Временные шаги: {time_steps}\n")
            self.info_text.insert(tk.END, f"✓ Площадь заражения через 5 шагов: ~")
            
            # Приблизительный расчет площади
            total_area = sum(np.pi * (s['radius'] + spread_speed * 5)**2 for s in self.sources)
            self.info_text.insert(tk.END, f"{total_area:.2f} кв.ед.\n")
            self.info_text.see(tk.END)
            
            self.status_var.set("Прогноз распространенения построен")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при прогнозе:\n{str(e)}")
            
    def clear_data(self):
        """Очистка всех данных"""
        self.points = None
        self.sources = None
        self.prediction_points = None
        
        self.ax1.clear()
        self.ax1.set_title('Карта зараженных точек')
        self.ax1.grid(True, alpha=0.3)
        self.canvas1.draw()
        
        self.ax2.clear()
        self.ax2.set_title('Прогноз распространения')
        self.ax2.grid(True, alpha=0.3)
        self.canvas2.draw()
        
        self.info_text.delete(1.0, tk.END)
        self.status_var.set("Данные очищены")
        self.analyze_btn.config(state=tk.DISABLED)
        self.predict_btn.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = InfectionSpreadApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
