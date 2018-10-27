//
//  TableViewRowAction.swift
//  Pinky
//
//  Created by 山川拓也 on 2018/10/27.
//  Copyright © 2018 山川拓也. All rights reserved.
//

import UIKit

class TableViewRowAction: UITableViewRowAction{
    var image: UIImage?
    
    func _setButton(button: UIButton)
    {
        if let image = image, let titleLabel = button.titleLabel
        {
            let labelString = NSString(string: titleLabel.text!)
            let titleSize = labelString.size(withAttributes: [NSAttributedString.Key.font: titleLabel.font])
            
            button.tintColor = UIColor.white
            button.setImage(image.withRenderingMode(.alwaysTemplate), for: .normal)
            button.imageEdgeInsets.right = -titleSize.width
        }
    }
}
